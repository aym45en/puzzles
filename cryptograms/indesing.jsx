// InDesign Script

// Function to read the text file
function readFile(filePath) {
    var file = new File(filePath);
    file.open('r');
    var content = file.read();
    file.close();
    return content;
}

// Function to create a new text frame with specific text
function createTextFrame(page, content, number, topPosition, arialFont,verticalSpacing, pageWidth, leftMargin, rightMargin) {
    var textFrame = page.textFrames.add();
    var frameHeight = verticalSpacing; // Height of each text frame in points
    var frameWidth = pageWidth - leftMargin - rightMargin; // Width of each text frame considering margins

    textFrame.geometricBounds = [topPosition, leftMargin, topPosition + frameHeight, leftMargin + frameWidth];
    textFrame.contents = number + ". " + ' ' + content;

    // Center the text frame content
    textFrame.textFramePreferences.verticalJustification = VerticalJustification.CENTER_ALIGN;

    // Apply paragraph style to make the number large and add space between lines
    var paragraph = textFrame.paragraphs.item(0);
    var firstWord = paragraph.words.item(0);
    firstWord.fontStyle = "Bold"; // Make the number bold

    // Apply paragraph alignment and set font and leading
    paragraph.justification = Justification.CENTER_ALIGN;
    paragraph.appliedFont = arialFont;
    paragraph.leading = 40; // Add extra space between lines
    paragraph.pointSize = 16;
    paragraph.hyphenation = false;

}

// Main Script
var filePath = File.openDialog("Select your text file", "*.txt");
if (filePath !== null) {
    var doc = app.documents.add();

    // Assuming default page size and margins are already set in document preferences
    var pageWidth = doc.documentPreferences.pageWidth;
    var pageHeight = doc.documentPreferences.pageHeight;
    var leftMargin = doc.marginPreferences.left;
    var rightMargin = doc.marginPreferences.right;
    var topMargin = doc.marginPreferences.top;
    var bottomMargin = doc.marginPreferences.bottom;

    // Set default language to English
    doc.textDefaults.appliedLanguage = "English: USA";

    var content = readFile(filePath).split('\n');
    var paragraphsPerPage = 2;
    var verticalSpacing = (pageHeight - topMargin - bottomMargin) / paragraphsPerPage;

    // Set default Arial font
    var arialFont = "Arial";

    for (var i = 0; i < content.length; i++) {
        if (i % paragraphsPerPage === 0 && i !== 0) {
            doc.pages.add();
        }

        var currentPage = doc.pages.item(Math.floor(i / paragraphsPerPage));
        var topPosition = topMargin + (i % paragraphsPerPage) * verticalSpacing;

        createTextFrame(currentPage, content[i], (i + 1).toString(), topPosition, arialFont, verticalSpacing, pageWidth, leftMargin, rightMargin);
    }
}
