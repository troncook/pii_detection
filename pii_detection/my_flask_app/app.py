from flask import Flask, request, render_template
from transformers import pipeline

app = Flask(__name__)

# Load the model using a pipeline
pipe = pipeline("token-classification", model="brettlin/distilbert-base-uncased-finetuned-ner")

labels = ['O', 'B-O', 'I-O', 'L-O', 'U-O', 'B-PER', 'I-PER', 'L-PER', 'U-PER', 'B-LOC', 'I-LOC', 'L-LOC', 'U-LOC', 
          'B-ORG', 'I-ORG', 'L-ORG', 'U-ORG', 'B-NRP', 'I-NRP', 'L-NRP', 'U-NRP', 'B-DATE_TIME', 'I-DATE_TIME', 
          'L-DATE_TIME', 'U-DATE_TIME', 'B-CREDIT_CARD', 'I-CREDIT_CARD', 'L-CREDIT_CARD', 'U-CREDIT_CARD', 'B-URL', 
          'I-URL', 'L-URL', 'U-URL', 'B-IBAN_CODE', 'I-IBAN_CODE', 'L-IBAN_CODE', 'U-IBAN_CODE', 'B-US_BANK_NUMBER', 
          'I-US_BANK_NUMBER', 'L-US_BANK_NUMBER', 'U-US_BANK_NUMBER', 'B-PHONE_NUMBER', 'I-PHONE_NUMBER', 'L-PHONE_NUMBER',
          'U-PHONE_NUMBER', 'B-US_SSN', 'I-US_SSN', 'L-US_SSN', 'U-US_SSN', 'B-US_PASSPORT', 'I-US_PASSPORT', 'L-US_PASSPORT',
          'U-US_PASSPORT', 'B-US_DRIVER_LICENSE', 'I-US_DRIVER_LICENSE', 'L-US_DRIVER_LICENSE', 'U-US_DRIVER_LICENSE',
          'B-US_LICENSE_PLATE', 'I-US_LICENSE_PLATE', 'L-US_LICENSE_PLATE', 'U-US_LICENSE_PLATE', 'B-IP_ADDRESS', 'I-IP_ADDRESS',
          'L-IP_ADDRESS', 'U-IP_ADDRESS', 'B-US_ITIN', 'I-US_ITIN', 'L-US_ITIN', 'U-US_ITIN', 'B-EMAIL_ADDRESS', 'I-EMAIL_ADDRESS',
          'L-EMAIL_ADDRESS', 'U-EMAIL_ADDRESS', 'B-TITLE', 'I-TITLE', 'L-TITLE', 'U-TITLE', 'B-COORDINATE', 'I-COORDINATE', 'L-COORDINATE',
          'U-COORDINATE', 'B-IMEI', 'I-IMEI', 'L-IMEI', 'U-IMEI', 'B-PASSWORD', 'I-PASSWORD', 'L-PASSWORD', 'U-PASSWORD', 'B-LICENSE_PLATE',
          'I-LICENSE_PLATE', 'L-LICENSE_PLATE', 'U-LICENSE_PLATE', 'B-CURRENCY', 'I-CURRENCY', 'L-CURRENCY', 'U-CURRENCY', 'B-FINANCIAL',
          'I-FINANCIAL', 'L-FINANCIAL', 'U-FINANCIAL', 'B-ROUTING_NUMBER', 'I-ROUTING_NUMBER', 'L-ROUTING_NUMBER', 'U-ROUTING_NUMBER',
          'B-SWIFT_CODE', 'I-SWIFT_CODE', 'L-SWIFT_CODE', 'U-SWIFT_CODE', 'B-MAC_ADDRESS', 'I-MAC_ADDRESS', 'L-MAC_ADDRESS', 'U-MAC_ADDRESS',
          'B-AGE', 'I-AGE', 'L-AGE', 'U-AGE']

def map_indices_to_labels(indices):
    mapped_labels = []
    for i in indices:
        try:
            mapped_labels.append(labels.index(i))
        except ValueError:
            print(f"Warning: {i} not found in labels list")
            # You could also append a default value here if necessary
    return mapped_labels

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_text():
    text = request.form['text']

    if not text:
        return "No text provided", 400

    results = pipe(text)
    
    print(results)  # This line is for inspecting the structure of results

    # Assuming 'entity' is the correct key in results to get the entity indices
    indices = [result['entity'] for result in results]  

    mapped_labels = map_indices_to_labels(indices)

    # Process the results here (use mapped_labels)
    processed_results = ', '.join([labels[i] for i in mapped_labels])

    return render_template('result.html', results=results, mapped_labels=processed_results)

if __name__ == '__main__':
    app.run()








