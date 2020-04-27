
import argparse
import logging
import os
import numpy as np
import random
import sys
import collections

import pulp
import editdistance

import json
import spacy
import itertools

from tqdm import tqdm


def editdist(p_pred, p_gold):
    return 1 - (editdistance.eval(p_pred, p_gold) / max(len(p_pred), len(p_gold)))


def print_alignment(pred, true, a_pred, a_true):
    for k in a_pred:
        print(a_pred[k][1], pred[k], "<=>", true[a_pred[k][0]] if a_pred[k][0] is not None else None)

    for k in a_true:
        if a_true[k][0] is not None:
            continue

        print(a_true[k][1], pred[a_true[k][0]] if a_true[k][0] is not None else None, "<=>", true[k])


class Evaluator:
    def __init__(self, args, dim):
        self.args = args
        self.sim = editdist
        self.dim = dim

    def evaluate(self, pred, true):
        precs, recalls, fs = [], [], []

        for k in tqdm(list(true.keys())):
            if self.args.ignore_missing and k not in pred["re"]:
                continue

            #
            # Calculate score for each reference and choose the best one.
            local_precs, local_recalls, local_fs = [], [], []
            local_trues, local_a_pred, local_a_true = [], [], []
            local_num_cor = []

            y_pred = [rf for _, _, rf in pred["re"][k]]
            refs_idx = range(3)
            refs_idx = random.sample(refs_idx, self.args.nb_references)

            for ref_no in refs_idx:
                y_true = [rf for _, _, rf in true[k][ref_no]]

                num_cor, a_pred, a_true = self.best_alignment(y_pred, y_true)
                prec, recall = num_cor / len(y_pred) if len(y_pred) > 0 else 0, num_cor / len(y_true) if len(y_true) > 0 else 0
                f = (2 * prec * recall) / (prec + recall) if prec + recall > 0 else 0

                local_precs += [prec]
                local_recalls += [recall]
                local_fs += [f]
                local_trues += [y_true]
                local_a_pred += [a_pred]
                local_a_true += [a_true]
                local_num_cor += [num_cor]

            best_ref_no = np.argmax(local_num_cor)
            prec, recall, f = local_precs[best_ref_no], local_recalls[best_ref_no], local_fs[best_ref_no]
            y_true = local_trues[best_ref_no]

            if self.args.verbose == 1:
                print("-" * 3)
                print(local_fs)
                print("P:", prec, "R:", recall, "F:", f)
                print("Pred:", y_pred)
                print("True:", y_true)
                print("Alignment:")
                print_alignment(y_pred, y_true, local_a_pred[best_ref_no], local_a_true[best_ref_no])

            precs += [prec]
            recalls += [recall]
            fs += [(2 * prec * recall) / (prec + recall) if prec + recall > 0 else 0]

        return {"prec": np.mean(precs), "recall": np.mean(recalls), "f1": np.mean(fs)}

    def best_alignment(self, di, dj):
        problem = pulp.LpProblem("Problem-1", pulp.LpMaximize)

        # Variable
        alignment = [[pulp.LpVariable("align_{}_{}".format(i, j), 0, 1, pulp.LpBinary) for j in range(len(dj))] for i in
                     range(len(di))]

        #
        # Constraints

        # Each node has one out going edge
        for i in range(len(di)):
            y = 0

            if len(dj) == 0:
                continue

            for j in range(len(dj)):
                y += alignment[i][j]

            problem.addConstraint(y <= 1)

        # Each node has one out going edge
        for i in range(len(dj)):
            y = 0

            if len(di) == 0:
                continue

            for j in range(len(di)):
                y += alignment[j][i]

            problem.addConstraint(y <= 1)

        # Set objective function.
        obj_vars = []
        obj_coefs = collections.defaultdict(dict)

        for i in range(len(di)):
            for j in range(len(dj)):
                coefs = []

                if "e" in self.dim: coefs += [self.sim(di[i][0], dj[j][0]), self.sim(di[i][2], dj[j][2])]
                if "r" in self.dim: coefs += [self.sim(di[i][1], dj[j][1])]

                coef = np.mean(coefs)

                obj_coefs[i][j] = coef

                if coef > 0.0:
                    obj_vars += [coef * alignment[i][j]]

        if len(obj_vars) == 0:
            return 0.0, {}, {}

        problem.setObjective(sum(obj_vars))
        problem.solve()

        alignment_pred, alignment_true = {}, {}

        for i in range(len(di)):
            alignment_pred[i] = None, 0.0

            for j in range(len(dj)):
                if pulp.value(alignment[i][j]) == 1.0:
                    alignment_pred[i] = j, obj_coefs[i][j]

        for i in range(len(dj)):
            alignment_true[i] = None, 0.0

            for j in range(len(di)):
                if pulp.value(alignment[j][i]) == 1.0:
                    alignment_true[i] = j, obj_coefs[j][i]

        num_cor = pulp.value(problem.objective)
        return num_cor, alignment_pred, alignment_true



def main(args):
    preds = json.load(open(args.prediction))
    labels = json.load(open(args.label))

    random.seed(3)
    out = {}

    for k in ["e", "r", "er"]:
        eva = Evaluator(args, dim=k)
        ret = eva.evaluate(preds, labels)
        out[k] = ret

    print(json.dumps(out))


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s- %(name)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-pred', '--prediction', required=True,
        help="Model prediction.")
    parser.add_argument(
        '-label', '--label', required=True,
        help="Gold-standard reasoning steps.")
    parser.add_argument(
        '-nbref', '--nb-references', default=3, type=int,
        help="Number of reference derivations.")
    parser.add_argument(
        '-ig', '--ignore-missing', action="store_true",
        help="Ignore missing predictions.")
    parser.add_argument(
        '-v', '--verbose', type=int, default=0,
        help="Verbose level.")
    args = parser.parse_args()

    main(args)
