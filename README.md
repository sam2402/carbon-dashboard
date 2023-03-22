# Carbon Dashboard
### Deployment Manuel
1. Clone this repository

2. Follow the instructions here to install the Azure CLI
[How to install the Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)

3. Once this is installed, open your command line and enter

 `az login` 

 Following the instructions to login to your Microsoft account.
 
 If you are Adamos Hadjivasiliou, Yun Fu or Dean Mohamedally, you should have been given access to our system by our client Avanade. If you encounter errors when logging in or when running our dashboard please contact me at [sam.lavadera.20@ucl.ac.uk](mailto:sam.lavadera.20@ucl.ac.uk).

4. Go to the directory `carbon-dashboard` you created by cloning this repository. Start the server by running the following commands:
```
cd backend
./server
```

5. After a few seconds the following will appear in your command line:

 ```Running on http://127.0.0.1:5000```
 
 Go to http://127.0.0.1:5000/ in your browser

6. Go back to your terminal in which you started the server. Wait until you see "SERVER READY!" in your terminal. **This will take several minutes.**

7. Keeping the server running, open a new terminal window in the `carbon-dashboard` directory.

8. Run the following
```
cd frontend
npm install
npm start
```

9. Open http://localhost:3000 in your browser.

10. You will now see the carbon dashboard! Some graphs and figures may take up to a minute to load especially the first time you open a page. After this it will speed up as we have implemented a cache on the backend for common requests.