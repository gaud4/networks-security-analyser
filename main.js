const { app, BrowserWindow, ipcMain } = require("electron");
const fs = require("fs");
const path = require("path");

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  win.loadFile("index.html");
}

ipcMain.on("run-background-task", async (event) => {
  const totalSteps = 3;
  for (let i = 0; i <= totalSteps; i++) {
    await new Promise((resolve) => setTimeout(resolve, 500));
    event.sender.send("progress", (i / totalSteps) * 100);
  }

  // Read the content of the text file
  const filePath = path.join(__dirname, "data.txt");
  fs.readFile(filePath, "utf-8", (err, data) => {
    if (err) {
      console.error("Error reading file:", err);
      event.sender.send("task-completed", ["Error reading file"]);
      return;
    }

    // Split data by the delimiter
    const sections = data.split("--------------------------------------");
    event.sender.send("task-completed", sections);
  });
});

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
