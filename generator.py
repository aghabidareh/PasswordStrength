# dataset : kaggle.com/datasets/wjburns/common-password-list-rockyoutxt

import pandas as pd
import string
import re

def read_passwords(file_path):
    with open(file_path, "r", encoding="ISO-8859-1") as file:
        return [line.strip() for line in file.readlines()]
    
def is_common_password(password):
    common_passwords = {'12345', 'password', 'qwerty', 'letmein', 'welcome'}
    return password in common_passwords or re.search(r'(.)\1{2,}', password)

def check_complexity(password):
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    return has_upper, has_lower, has_digit, has_special

# طبقه‌بندی پسوورد
def label_password(password):
    length = len(password)
    has_upper, has_lower, has_digit, has_special = check_complexity(password)
    
    if length < 6 or is_common_password(password) or (not has_upper and not has_lower and not has_digit):
        return 'very weak'
    
    if length <= 8:
        if not has_digit or not has_special:
            return 'weak'
        if has_upper and not has_lower:
            return 'weak'
    
    if length <= 12:
        if has_digit and not has_special:
            return 'middle'
        if has_upper and has_lower:
            return 'middle'
    
    if length > 12:
        if has_upper and has_lower and has_digit and has_special:
            return 'good'
    
    if length > 12:
        if has_upper and has_lower:
            return 'powerful'
    
    return 'good'

def create_labeled_dataset(passwords):
    return [{'password': pw, 'strength': label_password(pw)} for pw in passwords]

def save_to_csv(dataset, output_file):
    df = pd.DataFrame(dataset)
    df.to_csv(output_file, index=False)
    
def main():
    passwords = read_passwords('passwords.txt')
    labeled_data = create_labeled_dataset(passwords)
    save_to_csv(labeled_data, 'passwords.csv')
    
if __name__ == "__main__":
    main()