from torchvision import transforms

from model import UNet
from dataset import *

from util import show_tensor_img

lr = 1e-3
num_epoch = 100

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = UNet(nch=3, nker=64, norm="bnorm", learning_type="plain")

transform_train = transforms.Compose([Normalization(), ToTensor(), Padding()])

dataset_train = Dataset(label_dir="test/data/label", input_dir="test/data/input", transform=transform_train)

loader_train = DataLoader(dataset_train, batch_size=1, shuffle=True, num_workers=0)

fn_loss = nn.MSELoss().to(device)

optim = torch.optim.Adam(model.parameters(), lr=lr)

loss_lst = []

for epoch in range(num_epoch + 1):
    for batch, data in enumerate(loader_train, 1):
        label = data['label'].to(device)
        input = data['input'].to(device)

        output = model(input)

        optim.zero_grad()

        loss = fn_loss(output, label)
        loss.backward()

        optim.step()

        loss_lst += [loss.item()]

    print(epoch, loss.item())
show_tensor_img(label)
show_tensor_img(input)
show_tensor_img(output)

plt.plot(range(len(loss_lst)), loss_lst, color="blue")
plt.show()
