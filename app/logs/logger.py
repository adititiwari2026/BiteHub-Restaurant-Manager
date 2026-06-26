def write_logs(data):
    
    with open("order.txt", 'a') as file:
        # striftime ko strftime kiya gaya hai
        errordata = {
            "DateTime": datetime.datetime.now().strftime("%d-%m-%y"), 
            "LogType": "ERROR",
            "ErrorMessage": str(data)
        }
        # Dictionary ko string mein convert karke likhein
        file.write(str(errordata) + "\n")