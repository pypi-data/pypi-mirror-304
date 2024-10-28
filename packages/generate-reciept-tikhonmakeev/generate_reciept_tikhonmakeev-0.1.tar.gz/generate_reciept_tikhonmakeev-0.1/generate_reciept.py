import argparse
import json

def generate_receipt(input_file: str, output_file: str):
    with open(input_file, 'r', encoding='utf-8') as file:
        order_data = json.load(file)
    
    customer_name = order_data['customer_name']
    items = order_data['items']
    total = sum(item['quantity'] * item['price'] for item in items)
    
    check_lines = []
    check_lines.append(f"Клиент: {customer_name}")
    check_lines.append("Товары:")
    
    for item in items:
        name = item['name']
        quantity = item['quantity']
        price = item['price']
        check_lines.append(f"- {name}, {quantity} шт., {price} руб. за единицу")
    
    check_lines.append(f"Итого: {total} руб.")
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(check_lines))
    
    print(f"Чек сохранён в файл {output_file}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input-file', 
        type=str, 
        required=True)
    parser.add_argument(
        '--output-file', 
        type=str, 
        required=True)

    args = parser.parse_args()

    generate_receipt(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
