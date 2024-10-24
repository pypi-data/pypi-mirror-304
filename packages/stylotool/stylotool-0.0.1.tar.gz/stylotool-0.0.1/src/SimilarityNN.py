import torch.nn as nn
class SimilarityNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_hidden, output_dim):
        super(SimilarityNN, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_hidden = num_hidden
        self.output_dim = output_dim

        self.input_layer = nn.Linear(input_dim, hidden_dim)
        self.hidden_layers = [nn.Linear(hidden_dim, hidden_dim)]
        for i in range(1, num_hidden):
            self.hidden_layers.append(nn.Linear(hidden_dim, hidden_dim))
        self.output_layer = nn.Linear(hidden_dim, self.output_dim)

    def forward(self, data):
        intermediate = [nn.ReLU()(self.input_layer(data))]
        for i in range(self.num_hidden):
            intermediate.append(nn.ReLU()(self.hidden_layers[i](intermediate[i])))
        out = self.output_layer(intermediate[-1])
        return out
