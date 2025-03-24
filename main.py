import tkinter, requests, ctypes

try:
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
except:
    pass
def download_asset():
    asset_id = entry.get()
    url = f"https://assetdelivery.roblox.com/v1/asset/?id={asset_id}"
    
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            content_disposition = response.headers.get("Content-Disposition")
            if content_disposition and "filename=" in content_disposition:
                filename = content_disposition.split("filename=")[1].strip('"')
            else:
                filename = f"{asset_id}.rbxm"
            
            save_path = tkinter.filedialog.asksaveasfilename(
                defaultextension=".*",
                initialfile=filename,
                filetypes=[("RBXM File", "*.rbxm"),("RBXMX File", "*.rbxmx"),("All Files", "*.*")]
            )
            
            if save_path:
                with open(save_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
                result_label.config(text=f"File saved to {save_path}", fg="green")
            else:
                result_label.config(text="Download canceled.", fg="orange")
        else:
            result_label.config(text=f"Error: {response.status_code} - {response.reason}", fg="red")
    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Error: {str(e)}", fg="red")

# Create the main window
root = tkinter.Tk()
root.title("Roblox Asset Downloader")
root.geometry("320x200")

label = tkinter.Label(root, text="Enter Asset ID:")
label.pack(pady=20)

entry = tkinter.Entry(root)
entry.pack(pady=10)

download_button = tkinter.Button(root, text="Download", command=download_asset)
download_button.pack(pady=20)

result_label = tkinter.Label(root, text="", fg="black")
result_label.pack(pady=10)

root.mainloop()