import torch
import storch
from torch.distributions import Bernoulli, Normal
from storch.method import ScoreFunction, Expect, UnorderedSetEstimator, GumbelSoftmax

p = torch.tensor([0.5], requires_grad=True)  # use array otherwise some estimators break
optim = torch.optim.SGD([p], lr=1.0)


# fixed p / no optimization
def choose(label, args) -> storch.method.Method:
    if args["method"] == "gumbel":
        return GumbelSoftmax(label, n_samples=args["samples"])
    if args["method"] == "gumbel_sparse":
        return storch.method.GumbelSparseMax(label, n_samples=args["samples"])
    if args["method"] == "gumbel_entmax":
        return storch.method.GumbelEntmax(
            "z", n_samples=args["samples"], adaptive=True
        )
    elif args["method"] == "gumbel_straight":
        return GumbelSoftmax(label, n_samples=args["samples"], straight_through=True)
    elif args["method"] == "gumbel_wor":
        return storch.method.UnorderedSetGumbelSoftmax(label, k=args["samples"])
    elif args["method"] == "score":
        return ScoreFunction(
            label, n_samples=args["samples"], baseline_factory=args["baseline"]
        )
    elif args["method"] == "expect":
        return Expect(label)
    elif args["method"] == "relax":
        return storch.method.RELAX(label, n_samples=args["samples"], in_dim=(args["latents"],))
    elif args["method"] == "rebar":
        return storch.method.REBAR(label, n_samples=args["samples"])
    elif args["method"] == "relax_rebar":
        return RELAX(
            label, n_samples=args["samples"], in_dim=(args["latents"],), rebar=True
        )
    elif args["method"] == "score_wor":
        return storch.method.ScoreFunctionWOR(label, k=args["samples"], use_baseline=False)
    elif args["method"] == "unordered":
        return UnorderedSetEstimator(label, k=args["samples"])
    elif args["method"] == "arm":
        return storch.method.ARM(label, n_samples=args["samples"])
    elif args["method"] == "disarm":
        return storch.method.DisARM(label, n_samples=args["samples"])
    else:
        raise ValueError("Invalid method passed to program arguments.")


def experiment(args):
    optim.zero_grad()
    m = choose("X1", args)

    b1 = Bernoulli(probs=p)
    X1 = m(b1)

    b2 = Bernoulli(probs=X1 / 2)
    X2 = choose("X2", args)(b2)

    cost = X2  # (x - x0) ** 2
    cost_node = storch.add_cost(cost, "cost")
    storch.backward()
    return p.grad.clone()


true_grad = experiment({"method": "expect"})
print("True gradient", true_grad)
print()

nsamples = 10

score_job = ("score", {"method": "score", "samples": nsamples, "baseline": None})
score_moving_job = ("score moving", {"method": "score", "samples": nsamples, "baseline": "moving_average"})
score_batch_job = ("score batch", {"method": "score", "samples": nsamples, "baseline": "batch_average"})
arm_job = ("arm", {"method": "arm", "samples": nsamples})
unordered_job = ("unordered", {"method": "unordered", "samples": nsamples})

# not working jobs:
relax_job = ("rebar", {"method": "rebar", "samples": nsamples})
gumbel_job = ("gumbel", {"method": "gumbel_straight",
                         "samples": nsamples})  # is gumbel expected to fail? does any variant of gumbel work? if we apply gumbel to every stochastic node, surely reparametrization should work?
disarm_job = ("disarm", {"method": "disarm", "samples": nsamples})
scorewor_job = ("score_wor", {"method": "score_wor", "samples": nsamples})  # don't know what this does

for job in [relax_job]:
    gradients = []
    print("Method:", job[0])
    # try:
    for i in range(1000):
        gradients.append(experiment(job[1]).unsqueeze(0))
    gradients = torch.cat(gradients)
    print("variance", gradients.var(0))
    print("mean gradient", gradients.mean(0))
    print("bias", torch.sum((gradients.mean(0) - true_grad) ** 2))
    # except Exception as err:
    #     print(err)
    print()

# """
# Based on Liu et al 2019, Kool et al 2020
# """
#
# import torch
# import storch
# from torch.distributions import Bernoulli
# from storch.method import ScoreFunction, Expect, UnorderedSetEstimator, GumbelSoftmax
#
# # x0 = torch.tensor(0.6)
# p = torch.tensor(0.5, requires_grad=True)
# # eta = torch.tensor(-0.0, requires_grad=True)
# # 0.4 with probability p, and 0.6 with probability 1-p
# # 0.16 * p + 0.36 * (1-p) = 0.36 - 0.2 * p.
# optim = torch.optim.SGD([p], lr=1.0)
#
#
# # fixed p / no optimization
# def choose(label, args) -> storch.method.Method:
#     if args["method"] == "gumbel":
#         return GumbelSoftmax(label, n_samples=args["samples"])
#     if args["method"] == "gumbel_sparse":
#         return storch.method.GumbelSparseMax(label, n_samples=args["samples"])
#     if args["method"] == "gumbel_entmax":
#         return storch.method.GumbelEntmax(
#             "z", n_samples=args["samples"], adaptive=True
#         )
#     elif args["method"] == "gumbel_straight":
#         return GumbelSoftmax(label, n_samples=args["samples"], straight_through=True)
#     elif args["method"] == "gumbel_wor":
#         return storch.method.UnorderedSetGumbelSoftmax(label, k=args["samples"])
#     elif args["method"] == "score":
#         return ScoreFunction(
#             label, n_samples=args["samples"], baseline_factory=args["baseline"]
#         )
#     elif args["method"] == "expect":
#         return Expect(label)
#     elif args["method"] == "relax":
#         return storch.method.RELAX(label, n_samples=args["samples"], in_dim=(args["latents"],))
#     elif args["method"] == "rebar":
#         return storch.method.REBAR(label, n_samples=args["samples"])
#     elif args["method"] == "relax_rebar":
#         return RELAX(
#             label, n_samples=args["samples"], in_dim=(args["latents"],), rebar=True
#         )
#     elif args["method"] == "score_wor":
#         return storch.method.ScoreFunctionWOR(label, k=args["samples"])
#     elif args["method"] == "unordered":
#         return UnorderedSetEstimator(label, k=args["samples"])
#     elif args["method"] == "arm":
#         return storch.method.ARM(label, n_samples=args["samples"])
#     elif args["method"] == "disarm":
#         return storch.method.DisARM(label, n_samples=args["samples"])
#     else:
#         raise ValueError("Invalid method passed to program arguments.")
#
#
# def experiment(args):
#     optim.zero_grad()
#
#     b1 = Bernoulli(probs=p)
#     X1 = choose("X1", args)(b1)
#
#     b2 = Bernoulli(probs=X1 / 2)
#     X2 = choose("X2", args)(b2)
#
#     cost = X1 + X2  # (x - x0) ** 2
#     storch.add_cost(cost, "cost")
#     storch.backward()
#     return p.grad.clone()
#
#
# true_grad = experiment({"method": "expect"})
# print("True gradient", true_grad)
# print()
#
# nsamples = 10
#
# score_job = ("score", {"method": "score", "samples": nsamples, "baseline": None})
# arm_job = ("arm", {"method": "arm", "samples": nsamples})
# # scorewor_job = ("score_wor", {"method": "score_wor", "samples": nsamples}) # don't know what this does
# gumbel_job = ("gumbel", {"method": "gumbel", "samples": nsamples})
# # rebar_job = ("relax", {"method": "relax", "samples": 2, "latents": 1}) # not working..
#
# for job in [ score_job, arm_job]:
#     gradients = []
#     print("Method:", job[0])
#     for i in range(1000):
#         gradients.append(experiment(job[1]).unsqueeze(0))
#     gradients = torch.cat(gradients)
#     print("variance", gradients.var(0))
#     print("mean gradient", gradients.mean(0))
#     print()
#     # print("bias", torch.sum((gradients.mean(0) - true_grad) ** 2))
