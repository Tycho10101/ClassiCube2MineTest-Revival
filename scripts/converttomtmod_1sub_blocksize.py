import argparse

parser = argparse.ArgumentParser()
parser.add_argument("MinX")
parser.add_argument("MinY")
parser.add_argument("MinZ")
parser.add_argument("MaxX")
parser.add_argument("MaxY")
parser.add_argument("MaxZ")

args = parser.parse_args()

MinX = float(args.MinX)
MinY = float(args.MinY)
MinZ = float(args.MinZ)
MaxX = float(args.MaxX)
MaxY = float(args.MaxY)
MaxZ = float(args.MaxZ)

MinX = MinX / 16
MinY = MinY / 16
MinZ = MinZ / 16
MaxX = MaxX / 16
MaxY = MaxY / 16
MaxZ = MaxZ / 16

MinX = MinX - 0.5
MinY = MinY - 0.5
MinZ = MinZ - 0.5
MaxX = MaxX - 0.5
MaxY = MaxY - 0.5
MaxZ = MaxZ - 0.5

print(str(MinX) + ", " + str(MinY) + ", " + str(MinZ) + ", " + str(MaxX) + ", " + str(MaxY) + ", " + str(MaxZ))