del lex-lambda-insurance-interns.zip 
cd lex-lambda-insurance-interns 
7z a -r ..\lex-lambda-insurance-interns.zip *
cd .. 
aws lambda update-function-code --function-name lex-lambda-insurance-interns --zip-file fileb://lex-lambda-insurance-interns.zip