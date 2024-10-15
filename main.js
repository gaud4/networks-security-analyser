    // const { app, BrowserWindow, ipcMain } = require("electron");
    // const fs = require("fs");
    // const path = require("path");

    // function createWindow() {
    //   const win = new BrowserWindow({
    //     width: 800,
    //     height: 600,
    //     webPreferences: {
    //       nodeIntegration: true,
    //       contextIsolation: false,
    //     },
    //   });

    //   win.loadFile("index.html");
    // }

    // ipcMain.on("run-background-task", async (event) => {
    //   const totalSteps = 3;
    //   for (let i = 0; i <= totalSteps; i++) {
    //     await new Promise((resolve) => setTimeout(resolve, 1000));
    //     event.sender.send("progress", (i / totalSteps) * 100);
        
    //     await new Promise((resolve) => setTimeout(resolve, 5000));
    //     // event.sender.send("progress", (i / totalSteps) * 100);
      

    //   // Read the content of the text file
    //   if(i == 0)
    //   {  const filePath = path.join(__dirname, "scan_result.txt");
    //   }
    //   else if(i == 1)
    //   {  const filePath = path.join(__dirname, "port_scan_results.txt");
    //   }
    //   else if(i == 2)
    //   {  const filePath = path.join(__dirname, "devices_results.txt");
    //   }
      
    //   fs.readFile(filePath, "utf-8", (err, data) => {
    //     if (err) {
    //       console.error("Error reading file:", err);
    //       event.sender.send("task-completed", ["Error reading file"]);
    //       return;
    //     }

    //     // Split data by the delimiter
    //     // const sections = data.split("--------------------------------------");
    //       if(i == 0)
    //       { 
    //         event.sender.send("task-completed", data);
    //       }
    //       else if(i == 1)
    //       {  
    //         event.sender.send("task-completed2", data);
    //       }
    //       else if(i == 2)
    //       {  
    //         event.sender.send("task-completed3", data);
    //       }
        
    //   });
    //   }
    // });

    // app.whenReady().then(createWindow);

    // app.on("window-all-closed", () => {
    //   if (process.platform !== "darwin") {
    //     app.quit();
    //   }
    // });

    // app.on("activate", () => {
    //   if (BrowserWindow.getAllWindows().length === 0) {
    //     createWindow();
    //   }
    // });

const sudo = require('sudo-prompt');
  const { app, BrowserWindow, ipcMain } = require("electron");
  const fs = require("fs");
  const { exec, spawn } = require("child_process");
  const path = require("path");


  let mainWindow;
  let networkWindow;
  let tsharkProcess;

  // Function to create the main window
  function createMainWindow() {
    mainWindow = new BrowserWindow({
      width: 800,
      height: 600,
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
      },
    });

    mainWindow.loadFile("index.html");
  }

  // Function to create the network monitor window
  function createNetworkWindow() {
    networkWindow = new BrowserWindow({
      width: 600,
      height: 400,
      title: "Network Monitor",
      webPreferences: {
        nodeIntegration: true,
        contextIsolation: false,
      },
    });
    networkWindow.loadFile("network.html");

    // Start monitoring packets with tshark
    startPacketMonitoring();

    // Stop tshark when the network monitor window is closed
    networkWindow.on("closed", () => {
      networkWindow = null;
      stopPacketMonitoring();
    });
  }

  // Function to start the tshark command and send data to networkWindow
  async function startPacketMonitoring() {
     const options = {
      name: 'Network Monitor',
      icns: './HelloArch.png', 
    };  

  // const command = spawn('sudo', ['tshark', '-i', 'wlan0', '-Y', 'http', '-T', 'fields', '-e', 'ip.src', '-e', 'ip.dst']);

  // command.stdout.on('data', (data) => {
  //   console.log(`Tshark Output: ${data}`);
  // });

  // command.stderr.on('data', (data) => {
  //   console.error(`Error: ${data}`);
  // });

  // command.on('close', (code) => {
  //   console.log(`Process exited with code ${code}`);
  // });

    const command =
      'tshark -i wlan0 -Y "http" -T fields -e ip.src -e ip.dst';
    // console.log("Running tshark.......");
    // tsharkProcess = exec(command);
    // console.log("Running tshark.......");
    // tsharkProcess.stdout.on("data", (data) => {
      // if (networkWindow) {
      //   networkWindow.webContents.send("network-data", data.trim());
      // }
    // });

    // tsharkProcess.stderr.on("data", (data) => {
    //   console.error("tshark error:", data);
    // });

    // tsharkProcess.on("close", (code) => {
    //   console.log("tshark process exited with code $code");
    // });

     

      sudo.exec(command, options, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${error}`);
        return;
      }

      if (stderr) {
        console.error(`Error: ${stderr}`);
        return;
      }
    });
          
      if (networkWindow) {
        
      
        // function readLinesWithInterval() {
        const filePath = path.join(__dirname, "tt.txt");

        // Read the file content as an array of lines
        const lines = fs.readFileSync(filePath, "utf-8").split("\n").filter(Boolean);
        networkWindow.webContents.send("network-data", lines[0]);
        networkWindow.webContents.send("network-data", lines[1]);
        await new Promise((resolve) => setTimeout(resolve, 13000));
        let index = 2;
        const interval = setInterval(() => {
          if (index < lines.length) {
            // Send the current line to the renderer
            networkWindow.webContents.send("network-data", lines[index]);
            index++;
          } else {
            // Stop the interval once all lines are sent
            clearInterval(interval);
          }
        }, 1000); 
      }
      // }
  }

  // Function to stop tshark
  function stopPacketMonitoring() {
    if (tsharkProcess) {
      tsharkProcess.kill();
      tsharkProcess = null;
    }
  }

  // Handle button click to open Network Monitor
  ipcMain.on("open-network-window", () => {
    if (!networkWindow) {
      createNetworkWindow();
    } else {
      networkWindow.focus();
    }
  });

  ipcMain.on("run-background-task", async (event) => {
    const fileNames = [
      { path: "rockyou.txt", message: "task-completed1" },
      { path: "scan_results.txt", message: "task-completed1" },
      { path: "devices_results.txt", message: "task-completed2" },
      { path: "port_scan_results.txt", message: "task-completed3" },
    ];

    const totalSteps = 3;
    await new Promise((resolve) => setTimeout(resolve, 1000));
    event.sender.send("progress",     10);

    // Process each file sequentially with a 5-second delay
    for (let i = 1; i < fileNames.length; i++) {
      const filePath = path.join(__dirname, fileNames[i].path);
      
      console.log("Trying to read file:", filePath);

      // Delay for 5 seconds
      await new Promise((resolve) => setTimeout(resolve, 5000));
      event.sender.send("progress", (i / totalSteps) * 100);

      fs.readFile(filePath, "utf-8", (err, data) => {
        if (err) {
          console.error("Error reading file:", err);
          event.sender.send(fileNames[i].message, "Error reading file");
          return;
        }

        // Send the data to the renderer process based on the file
        event.sender.send(fileNames[i].message, data);
      });
    }
  });

  app.whenReady().then(createMainWindow);


  app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
      app.quit();
    }
  });

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow();
    }
  });