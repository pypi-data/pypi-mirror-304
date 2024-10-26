import onetouch as ot

data = ot.One2Three(None, None, "datasets/Dry_Bean_Dataset/Dry_Bean_Dataset.xlsx")

x = [1, 2, 3, 4, 5, 6, 7, 8, 9]

print(data.predict(x))
