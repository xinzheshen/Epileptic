import argparse

import torch
from models import SeizurePredict


def parse_args():
    parser = argparse.ArgumentParser(description="Epileptic Seizure Prediction")
    # training
    training = parser.add_argument_group('training setup')
    training.add_argument('--epochs', type=int, default=100,
                          help='Number of total epochs to run')
    training.add_argument('--epochs-per-checkpoint', type=int, default=50,
                          help='Number of epochs per checkpoint')
    training.add_argument('--seed', type=int, default=1234,
                          help='Seed for PyTorch random number generators')

    return parser.parse_known_args()


def main():
    args, _ = parse_args()

    torch.manual_seed(args.seed)
    x = torch.randn(10, 1, 1280, 23, requires_grad=True)
    y = torch.rand(10).bernoulli()

    model = SeizurePredict()

    learning_rate = 1e-4
    optimizer = torch.optim.RMSprop(model.parameters(), lr=learning_rate)

    loss_fn = torch.nn.functional.binary_cross_entropy

    for epoch in range(args.epochs):
        y_p = model(x)
        # print(y_p)

        loss = loss_fn(y_p, y)
        print("loss: ", loss.data)

        loss.backward()

        optimizer.zero_grad()
        optimizer.step()


if __name__ == '__main__':
    main()
