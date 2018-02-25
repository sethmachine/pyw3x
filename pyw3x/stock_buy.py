"""

"""

def solution(stocks):
    pairs = []
    for i in range(0, len(stocks)):
        for j in range(i + 1, len(stocks)):
            if stocks[j] >= stocks[i]:
                pair = (i, j, stocks[j] - stocks[i])
                pairs.append(pair)
    return max(pairs, key=lambda x: x[-1])

def solution2(stocks):
    pass


if __name__ == '__main__':
    d = [3,7,9,2,8,14,1,7]
    ans = [3, 5]
    a = solution(d)