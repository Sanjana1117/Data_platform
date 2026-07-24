import pandas as pd

OUTPUT = "data/generated/brands.csv"

brands = [
("Apple","USA",1976),
("Samsung","South Korea",1938),
("Dell","USA",1984),
("HP","USA",1939),
("Lenovo","China",1984),
("Asus","Taiwan",1989),
("Acer","Taiwan",1976),
("MSI","Taiwan",1986),
("LG","South Korea",1958),
("Sony","Japan",1946),
("OnePlus","China",2013),
("Xiaomi","China",2010),
("Realme","China",2018),
("Vivo","China",2009),
("Oppo","China",2004),
("Boat","India",2016),
("Noise","India",2014),
("JBL","USA",1946),
("Canon","Japan",1937),
("Nikon","Japan",1917),
("Logitech","Switzerland",1981),
("Philips","Netherlands",1891),
("Nike","USA",1964),
("Adidas","Germany",1949),
("Puma","Germany",1948),
("Wildcraft","India",1998),
("Prestige","India",1955),
("Borosil","India",1962),
("Milton","India",1972),
("Tata","India",1868),
]

df = pd.DataFrame(
    brands,
    columns=["brand_name", "country", "founded_year"]
)

df.insert(0, "brand_id", range(1, len(df) + 1))

df.to_csv(OUTPUT, index=False)

print("✅ brands.csv generated")