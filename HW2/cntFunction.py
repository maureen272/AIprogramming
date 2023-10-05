#def my_count(s, sub):
#	return s.count(sub)

def my_count(s, sub):
    cnt = 0
    start = 0

    while start < len(s):
        index = s.find(sub, start)

        if index == -1:
            break

        cnt += 1
        start = index + len(sub)

    return cnt


s = input()
sub = input()
print(s, sub, my_count(s, sub))
s