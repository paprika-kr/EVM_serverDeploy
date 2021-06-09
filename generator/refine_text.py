# 순서 문제 지문 완벽화
def type_order(text, answer):

    first_english = False
    C_chunk = False
    temp_str = ""
    alphabet = ''
    paren = ''
    chunk = []
    perfect_text = ""
    index = 0

    # 문제에서 시작 문장, A,B,C 지문 chunk 추출하여 chunk에 저장.
    while index < len(text):
        if ord('a') <= ord(text[index].lower()) <= ord('z'):
            first_english = True
        if first_english:
            if text[index] == '(':
                alphabet = text[index + 1]
                paren = text[index + 2]
                if alphabet == 'A' and paren == ')':
                    print(temp_str)
                    chunk.append(temp_str)
                    temp_str = ""
                    index += 3
                    continue
                elif (alphabet == 'B' and paren == ')'):
                    chunk.append(temp_str)
                    temp_str = ""
                    index += 3
                    continue
                elif (alphabet == 'C' and paren == ')'):
                    chunk.append(temp_str)
                    temp_str = ""
                    index += 3
                    C_chunk = True
                    continue
            elif text[index] == '\n':
                if (C_chunk):
                    if (text[index + 1] == '\n'):
                        break

                #개행인 경우 space 삽입
                temp_str += ' '
                index += 1
                continue
            temp_str += text[index]
            first_english = True
        index += 1
    chunk.append(temp_str)

    # 시작 문장 insert
    perfect_text = chunk[0]
    print(perfect_text)

    # A-C-B
    if answer == 1:
        perfect_text += chunk[1]
        perfect_text += chunk[3]
        perfect_text += chunk[2]
    # B-A-C
    elif answer == 2:
        perfect_text += chunk[2]
        perfect_text += chunk[1]
        perfect_text += chunk[3]
    # B-C-A
    elif answer == 3:
        perfect_text += chunk[2]
        perfect_text += chunk[3]
        perfect_text += chunk[1]
    # C-A-B
    elif answer == 4:
        perfect_text += chunk[3]
        perfect_text += chunk[1]
        perfect_text += chunk[2]
    # C-B-A
    elif answer == 5:
        perfect_text += chunk[3]
        perfect_text += chunk[2]
        perfect_text += chunk[1]

    return perfect_text


# 삽입 문제 지문 완벽화
def type_insert(text, answer):
    index = 0;
    ans_match = 0
    perfect_text = "";
    to_insert = ""

    # 삽입할 문장 시작점 찾기
    for i in range(len(text)):
        start_flag = True
        if text[i].encode().isalpha() == False:
            continue
        else:
            for j in range(1, 10):
                if (ord('가') <= ord(text[j + i]) <= ord('힣')):
                    start_flag = False
                    break
                else:
                    continue
            if start_flag == True:
                break
    # 삽입할 문장 저장, 본문 시작점 찾기
    for j in range(i, len(text)):
        if text[j] != '\n':
            to_insert += text[j]
            continue
        elif text[j] == '\n':
            if text[j + 1] == '\n':
                for k in range(j + 2, len(text)):
                    if text[k] != '\n':
                        break
                break
            else:
                continue
    print("삽입할문장: ", to_insert + '\n')  # 삽입할 문장 맞는지 확인용

    # k: 본문 시작점 인덱스, text에 본문만 다시 저장한다.
    text = text[k:]
    # 지문 시작부분에 공백이 있으면 제거.
    for i in range(len(text)):
        if text[i].isalnum() == False:
            text = text[i + 1:]
            if text[i + 1].isalnum() == False:
                continue
            else:
                break

    # 삽입해서 완성하기
    tmp_text = ""
    cnt = 1  # 현재 처리 중인 (번호)를 저장

    i = 0
    while (i < len(text)):
        # (번호) 부분 처리
        if text[i] == '(':
            for j in range(i, i + 10):
                if text[j] == ')':
                    for k in range(j + 1, j + 10):  # ')' 뒤에 또 ')'로 인식하는 경우
                        if text[k] == ')':
                            j = k  # 뒤에 나온 ')'가 진짜 괄호이므로 그 까지 지워야 함
                            break  # ')' 다음에 또 바로 '('가 나올 때가 있을까?
                    if cnt == answer:  # 현재 (번호) 가 정답일 경우
                        tmp_text = text[:i] + to_insert + text[j + 1:]
                        text = tmp_text
                        cnt += 1
                        break
                    else:  # 현재 (번호)가정답이 아닐경우
                        tmp_text = text[:i] + text[j + 1:]
                        text = tmp_text
                        cnt += 1
                        break
        i += 1
    # print(text)
    # 공백과 개행 제거
    text = text.strip().replace("\n", " ")
    return text


# 빈칸 문제 지문 완벽화
def type_blank(text, answer):
    tmp_text = text
    perfect_text = ''

    # 삽입할 문장 시작점 찾기
    i = 0
    for i in range(len(tmp_text)):
        start_flag = True
        if tmp_text[i].encode().isalpha() == False:
            continue
        else:
            for j in range(1, 10):
                if (ord('가') <= ord(tmp_text[j + i]) <= ord('힣')):
                    start_flag = False
                    break
                else:
                    continue
            if start_flag == True:
                break

    # 앞에 한글 문제 제외하고 첫 시작부터 text에 넣기.
    tmp_text = tmp_text[i:]
    tmp_text = tmp_text.strip()
    tmp_text = tmp_text.replace('  ','*')
    tmp_text = tmp_text.replace('\n\n','*')

    tmp_list = tmp_text.split('*')

    ## 빈간 전
    first_text = tmp_list[0]
    tmp_list.pop(0)
    tmp_list = list(filter(('').__ne__, tmp_list))

    ## 빈칸 후
    end_text = tmp_list[0]
    tmp_list.pop(0)
    tmp_list = '\n'.join(tmp_list)

    ## 정답 리스트
    answer_list = tmp_list.split('\n')[-5:]
    answer_text = answer_list[answer - 1]

    if answer_text.find('@') != -1:
        answer_text = answer_text.replace('@',"")

    perfect_text = first_text+ ' ' + answer_text+ ' '+ end_text
    perfect_text = perfect_text.split('\n')
    perfect_text = ' '.join(perfect_text)

    return perfect_text


## 요지, 주장, 주제 본문 추출
## 그 외에도 본문만 필요한 경우 모두 사용 가능
def type_subject(text):
    tmp_text = text
    for i in range(len(tmp_text)):
        start_flag = True
        if tmp_text[i].encode().isalpha() == False:
            continue
        else:
            for j in range(1, 30):
                if (ord('가') <= ord(tmp_text[j + i]) <= ord('힣')):
                    start_flag = False
                    break
                else:
                    continue
            if start_flag == True:
                break

    # 앞에 한글 문제 제외하고 첫 시작부터 text에 넣기.
    tmp_text = tmp_text[i:]

    # 지문 끝 부분 찾기
    end_idx = tmp_text.find('\n\n')

    flag = 0
    # end_idx후 버리는 부분이 발생하는 지 확인
    if '+' in tmp_text[end_idx:] :
        flag = 1
    elif '*' in tmp_text[end_idx:] :
        flag = 2
    else :
        flag = 0

    # 확인해보니 주석의 경우 '+'로 표기가 되고 남는 부분이 발생하는 경우가 있음
    # 그렇기에 + 앞의 부분을 살려서 결과 text에 붙이고 나서 strip 메서드를 통해서 빈공간 삭제
    if flag == 1 :
        need_text = tmp_text[end_idx:].split('+')[0]
        res_text = tmp_text[:end_idx] + ' '.join(need_text.split('\n'))
    elif flag == 2:
        need_text = tmp_text[end_idx:].split('*')[0]
        res_text = tmp_text[:end_idx] + ' '.join(need_text.split('\n'))
    else :
        res_text = tmp_text[:end_idx]
    res_text = res_text.strip()
    tmp_list = res_text.split('*')
    res_text = tmp_list[0]
    res_text = res_text.replace('\n',' ')

    return res_text
