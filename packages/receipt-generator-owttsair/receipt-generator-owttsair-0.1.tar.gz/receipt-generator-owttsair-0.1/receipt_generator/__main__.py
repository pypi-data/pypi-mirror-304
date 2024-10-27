import argparse
from .receipt import load_order, generate_receipt, save_receipt
def main():
    parser = argparse.ArgumentParser(description="Generate receipt from order JSON file.")
    parser.add_argument("--input-file", required=True, help="Path to input JSON file.")
    parser.add_argument("--output-file", required=True, help="Path to output receipt text file.")
    args = parser.parse_args()
    order_data = load_order(args.input_file)
    receipt_content = generate_receipt(order_data)
    save_receipt(receipt_content, args.output_file)
if __name__ == "__main__":
    main()
