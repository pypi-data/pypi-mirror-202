# 斗地主 54 20+17+17

import random
class Card:
    def __init__(self,txt,color,num):
        self.txt = txt
        self.color = color
        self.num = num

    def __repr__(self):
        return self.txt

    def __eq__(self, other):
        return self.txt == other.txt

txts = ["3","4","5","6","7","8","9","10","J","Q","K","A","2"]
colors = ["红桃","黑桃","方片","梅花"];
cards = []

for t in range(len(txts)):
    for c in colors:
        cards.append(Card(txts[t],c,t))

cards.append(Card("S","",14))
cards.append(Card("B","",15))

#print(cards)
random.shuffle(cards)
#print(cards)

list1 = cards[0:20]
list2 = cards[20:37]
list3 = cards[37:]

list1 = sorted(list1,key=lambda card: card.num)
list2 = sorted(list2,key=lambda card: card.num)
list3 = sorted(list3,key=lambda card: card.num)
all_list = [list1,list2,list3]

def print_all():
    print(list1)
    print(list2)
    print(list3)

#print_all()

current_index = 1;

def print_list():
   print(all_list[current_index-1])

def isOver():
    return len(list1)==0|len(list2)==0|len(list3)==0

def del_card(param):
    ccards = all_list[current_index-1].copy();
    for n in param:
        s = n;
        if(s=="1"):
            s = s+"0"
        if(s=="0"):
            continue
        if Card(s,"",0) not in ccards:
            return False
        else:
            ccards.remove(Card(s,"",0))

    for n in param:
        s = n;
        if (s == "1"):
            s = s + "0"
        if (s == "0"):
            continue
        all_list[current_index-1].remove(Card(s,"",0))
    return True

def test_start():
    while not isOver():
        print_list()
        cardstr = input("请您出牌：")
        print(cardstr)
        del_card(cardstr)
        current_index = current_index + 1
        if (current_index == 4):
            current_index = 1

if __name__ == "__main__":
    test_start()

# mycards = []
# mycards.append(Card("3","红桃",1))
# mycards.append(Card("3","黑桃",1))
# mycards.append(Card("4","红桃",2))
# mycards.append(Card("5","红桃",3))
# mycards.append(Card("K","红桃",11))
# mycards.append(Card("K","黑桃",11))
# mycards.append(Card("K","方片",11))





# if del_card("44"):
#     print("ok")
# else:
#     print("没有这样牌")
#
# print(mycards)


