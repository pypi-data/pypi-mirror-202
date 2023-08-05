class Kalkulator:
    def __init__(self):
        self.angka = 0

    def tambah(self,*args):
        self.angka = 0
        for i in args:
            self.angka += i
        return self.angka
    
    def kali(self, *args):
        self.angka = 1
        for i in args:
            self.angka *= i
        return self.angka

    def kurang(self, *args):
        self.angka = args[0] * 2
        for i in args:
            self.angka -= i
        return self.angka
        


    


if __name__ == '__main__':
    hitung = Kalkulator()
    print(hitung.kurang(12,2, 1))

