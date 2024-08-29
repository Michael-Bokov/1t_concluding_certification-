import os
import sys
from datetime import datetime

#path = "/home/user"
#корневой каталог.
path = path if 'path' in globals() else os.path.abspath(os.sep)
#Подсчитывает количество в каталоге и его подкаталогах
def count_files(directory):
    """ """
    file_count = 0
    for root, dirs, files in os.walk(directory):
        file_count += len(files)
    return file_count

def top_size(path):
    file_sizes=[]
    for root,dir,files in os.walk(path):
        for file in files:
            file_path=os.path.join(root,file)
            try:
                file_size = os.path.getsize(file_path)
                file_sizes.append((file_path, file_size))
            except (PermissionError, FileNotFoundError,OSError):
                # Игнорируем файлы, нет доступа
                continue
    return sorted(file_sizes, key=lambda x: x[1], reverse=True)[:10]

if __name__ == '__main__':
    name=''
    #имя из командной строки
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        print("No name provided")
    
    cur_date= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'Hello,{name}!')
    print(f'Current time: {cur_date}')
    print(f'Calculating...')

    file_count = count_files(path)
    print(f"Total number of files in {path}: {file_count}")

    # Выводим топ-10 файлов по размеру
    top_10_files = top_size(path)
    print("Top 10 largest files:")
    for file_path, size in top_10_files:
        print(f"{file_path}: {size:.2f} KB")
