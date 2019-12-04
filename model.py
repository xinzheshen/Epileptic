import torch


class DCNN(torch.nn.Module):
    def __init__(self):
        super(DCNN, self).__init__()
        self.n_layers = 4
        self.layers = torch.nn.ModuleList()
        self.pool = torch.nn.MaxPool2d(2)
        for i in range(self.n_layers):
            if i == 0:
                self.layers.append(torch.nn.Conv2d(1, 32, (2, 2)))
            else:
                self.layers.append(torch.nn.Conv2d(32, 32, (2, 2)))

    def forward(self, input):
        for i in range(self.n_layers):
            input = self.layers[i](input)
            if i < self.n_layers - 1:
                input = self.pool(input)

        return input


class BiLSTM(torch.nn.Module):
    def __init__(self):
        super(BiLSTM, self).__init__()

    def forward(self):
        pass


class SeizurePredict(torch.nn.Module):
    def __init__(self):
        super(SeizurePredict, self).__init__()

    def forward(self):
        pass