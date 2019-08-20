import re

def formating():
    f = open("comment.txt","r",encoding='UTF-8')
    fn = open('comment_wash.txt','w',encoding='UTF-8')
    
    for line in f :
        
        string_com_old_1 = line[25:-3]
        if not (bool(re.search(r'\\u', string_com_old_1, flags= 2)) or bool(re.search(r'video', string_com_old_1, flags= 2))):
            string_com_old_2 = re.sub(r'\\u003c', "<", string_com_old_1)
            string_com_old_3 = re.sub(r'\\u003e', ">", string_com_old_2)
            string_com_old_4 = re.sub(r'\\u0026', "&", string_com_old_3)
            string_com = re.sub(r'\\n', "", string_com_old_4)
            fn.write(string_com + "\n")

    f.close()
    fn.close()
        

if __name__=='__main__':
    formating()
    print("Well Done")
