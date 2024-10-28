import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;

public class SimpleNotepad extends JFrame implements ActionListener {
    JTextArea textArea;
    JFileChooser fileChooser;
    File currentFile;

    public SimpleNotepad() {
        setTitle("Simple Notepad");
        setVisible(true);
        setSize(800, 600);
        setDefaultCloseOperation(EXIT_ON_CLOSE);

        textArea = new JTextArea();
        add(new JScrollPane(textArea), BorderLayout.CENTER);

        JMenuBar menuBar = new JMenuBar();

        JMenu fileMenu = new JMenu("File");

        JMenuItem openItem = new JMenuItem("Open");
        JMenuItem saveItem = new JMenuItem("Save");
        JMenuItem saveAsItem = new JMenuItem("Save As");

        openItem.addActionListener(this);
        saveItem.addActionListener(this);
        saveAsItem.addActionListener(this);

        fileMenu.add(openItem);
        fileMenu.add(saveItem);
        fileMenu.add(saveAsItem);
        JMenu editMenu = new JMenu("Edit");

        JMenuItem cutItem = new JMenuItem("Cut");
        JMenuItem copyItem = new JMenuItem("Copy");
        JMenuItem pasteItem = new JMenuItem("Paste");

        cutItem.addActionListener(this);
        copyItem.addActionListener(this);
        pasteItem.addActionListener(this);

        editMenu.add(cutItem);
        editMenu.add(copyItem);
        editMenu.add(pasteItem);

        menuBar.add(fileMenu);
        menuBar.add(editMenu);

        setJMenuBar(menuBar);
        fileChooser = new JFileChooser();
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        String command = e.getActionCommand();
        switch (command) {
            case "Open":
                openFile();
                break;
            case "Save":
                saveFile();
                break;
            case "Save As":
                saveFileAs();
                break;
            case "Cut":
                textArea.cut();
                break;
            case "Copy":
                textArea.copy();
                break;
            case "Paste":
                textArea.paste();
                break;
        }
    }

    private void openFile() {
        int returnValue = fileChooser.showOpenDialog(this);
        if (returnValue == JFileChooser.APPROVE_OPTION) {
            currentFile = fileChooser.getSelectedFile();
            try (BufferedReader br = new BufferedReader(new FileReader(currentFile))) {
                textArea.read(br, null);
            } catch (IOException e) {
                JOptionPane.showMessageDialog(this, "Error opening file", "Error",
                        JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void saveFile() {
        if (currentFile != null) {
            try (BufferedWriter bw = new BufferedWriter(new FileWriter(currentFile))) {
                textArea.write(bw);
            } catch (IOException e) {
                JOptionPane.showMessageDialog(this, "Error saving file", "Error",
                        JOptionPane.ERROR_MESSAGE);
            }
        } else {
            saveFileAs();
        }
    }

    private void saveFileAs() {
        int returnValue = fileChooser.showSaveDialog(this);
        if (returnValue == JFileChooser.APPROVE_OPTION) {
            currentFile = fileChooser.getSelectedFile();
            saveFile();
        }
    }

    public static void main(String[] args) {
        new SimpleNotepad();
    }
}
