
import argparse
import logging

import json
import spacy
import sys
import re
import itertools

from tqdm import tqdm


class AllEntBaselineModel:
    def __init__(self):
        self.spacy_nlp = spacy.load("en_core_web_sm")

        self.spacy_nlp.add_pipe(self.spacy_nlp.create_pipe("merge_noun_chunks"))
        self.spacy_nlp.add_pipe(self.spacy_nlp.create_pipe("merge_entities"))

    def predict(self, inst, supporting_facts):
        ent2doc = dict(inst["context"])
        reasoning_steps = []

        for sup_ent, sup_sent_id in supporting_facts:
            if sup_sent_id > len(ent2doc[sup_ent]):
                continue

            sup_sent = list(self.spacy_nlp(ent2doc[sup_ent][sup_sent_id]).sents)

            if len(sup_sent) == 0:
                continue

            sup_sent = sup_sent[0]

            for np1 in sup_sent.noun_chunks:
                for np2 in sup_sent.noun_chunks:
                    if np1.start >= np2.start:
                        continue

                    reasoning_steps += [(
                        sup_ent,
                        sup_sent_id,
                        (
                            sup_ent if np1.text.lower() in ["she", "he", "it", "they"] else str(np1),
                            str(sup_sent[np1.end:np2.start]),
                            str(np2)
                        ),
                    )]

        return reasoning_steps


class DepBaselineModel:
    def __init__(self):
        self.spacy_nlp = spacy.load("en_core_web_sm")

        self.spacy_nlp.add_pipe(self.spacy_nlp.create_pipe("merge_noun_chunks"))
        self.spacy_nlp.add_pipe(self.spacy_nlp.create_pipe("merge_entities"))

    def extract_tuple(self, sent):
        rel = str(sent.root)
        obj = list(sent.root.rights)[0]

        if sent.root.tag_ == "VBN":
            rel = "is " + rel

        if obj.tag_ == "IN":
            rel += " " + str(obj)
            obj = list(obj.rights)[0]

        obj = str(obj)

        return rel, obj

    def predict(self, inst, supporting_facts):
        ent2doc = dict(inst["context"])
        reasoning_steps = []

        for sup_ent, sup_sent_id in supporting_facts:
            if sup_sent_id > len(ent2doc[sup_ent]):
                continue

            sup_sent = list(self.spacy_nlp(ent2doc[sup_ent][sup_sent_id]).sents)

            if len(sup_sent) == 0:
                continue

            sup_sent = sup_sent[0]

            if len(list(sup_sent.root.rights)) == 0:
                continue

            try:
                rel, obj = self.extract_tuple(sup_sent)

            except IndexError:
                rel, obj = None, None

            if rel is None:
                continue

            reasoning_steps += [(
                sup_ent,
                sup_sent_id,
                (sup_ent, rel, obj),
            )]

        return reasoning_steps


class OpenIEBaselineModel:
    def __init__(self):
        from openie import StanfordOpenIE
        self.openie_client = StanfordOpenIE()

        self.spacy_nlp = spacy.load("en_core_web_sm")

    def predict(self, inst, supporting_facts):
        ent2doc = dict(inst["context"])
        reasoning_steps = []

        for sup_ent, sup_sent_id in supporting_facts:
            if sup_sent_id > len(ent2doc[sup_ent]):
                continue
            #
            # sup_sent = list(self.spacy_nlp(ent2doc[sup_ent][sup_sent_id]).sents)
            #
            # if len(sup_sent) == 0:
            #     continue
            #
            # sup_sent = sup_sent[0]
            # sup_sent = [sup_ent if tk.text in ["it", "they", "she", "he"] else str(tk) for tk in sup_sent]
            # sup_sent = " ".join(sup_sent)
            sup_sent = ent2doc[sup_ent][sup_sent_id]

            for triplet in self.openie_client.annotate(sup_sent):
                if triplet["subject"] in ["it", "they", "she", "he"]:
                    triplet["subject"] = sup_ent

                reasoning_steps += [(
                    sup_ent,
                    sup_sent_id,
                    (triplet["subject"], triplet["relation"], triplet["object"]),
                )]

        return reasoning_steps


def main(args):
    tgt = json.load(open(args.input))

    if args.base_prediction is not None:
        base_pred = json.load(open(args.base_prediction))

    if args.reference is not None:
        ref = json.load(open(args.reference))

    bm = eval("{}BaselineModel()".format(args.model))

    out = {"answer": {}, "sp": {}, "re": {}}

    for inst in tqdm(tgt):
        if args.reference is not None:
            if inst["_id"] not in ref:
                continue

        if args.base_prediction is not None:
            if inst["_id"] in base_pred["answer"]:
                out["answer"][inst["_id"]] = base_pred["answer"][inst["_id"]]

            if inst["_id"] in base_pred["sp"]:
                out["sp"][inst["_id"]] = base_pred["sp"][inst["_id"]]

        else:
            out["answer"][inst["_id"]] = inst["answer"]
            out["sp"][inst["_id"]] = inst["supporting_facts"]

        if inst["_id"] in out["sp"]:
            out["re"][inst["_id"]] = bm.predict(inst, out["sp"][inst["_id"]])

        with open(args.output, "w") as f:
            print(json.dumps(out), file=f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-in', '--input', required=True,
        help="Input file.")
    parser.add_argument(
        '-base', '--base-prediction',
        help="Base prediction file.")
    parser.add_argument(
        '-out', '--output', required=True,
        help="Output file.")
    parser.add_argument(
        '-ref', '--reference',
        help="Reference file.")
    parser.add_argument(
        '-m', '--model', required=True,
        help="Mode type (Dep|OpenIE|AllEnt).")
    args = parser.parse_args()

    main(args)
