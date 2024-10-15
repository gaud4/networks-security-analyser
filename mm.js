const { exec } = require("child_process");

function runTsharkWithSudo() {
  const sudoPassword = 'Sardarji'; // Replace with your actual sudo password
  
  // Command to run tshark with sudo and HTTP filter
  const command = `echo ${sudoPassword} | sudo -S tshark -i wlan0 -Y "http" -T fields -e ip.src -e ip.dst
`;

  // Execute the command
  const process = exec(command);

  // Capture stdout (standard output) and display in console.log
  process.stdout.on('data', (data) => {
    console.log(`Tshark Output: ${data}`);
  });

  // Capture stderr (error output) and display in console.log
  process.stderr.on('data', (data) => {
    console.error(`Tshark Error: ${data}`);
  });

  // When the process finishes, log the exit code
  process.on('close', (code) => {
    console.log(`Tshark process exited with code ${code}`);
  });
}

// Run the function to start tshark with sudo
runTsharkWithSudo();
