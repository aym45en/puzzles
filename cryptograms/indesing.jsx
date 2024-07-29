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
function createTextFrame(page, content, number, position) {
    var textFrame = page.textFrames.add();
    textFrame.geometricBounds = position;
    textFrame.contents = number + ' ' + content;

    // Center the text frame content
    textFrame.textFramePreferences.verticalJustification = VerticalJustification.CENTER_ALIGN;

    // Apply paragraph style to make the number large and add space between lines
    var paragraph = textFrame.paragraphs.item(0);
    var firstWord = paragraph.words.item(0);
    firstWord.pointSize = 24; // Adjust the size as needed

    // Apply paragraph alignment
    paragraph.justification = Justification.CENTER_ALIGN;
    paragraph.leading = 24; // Add extra space between lines
}

// Main Script
var filePath = File.openDialog("Select your text file", "*.txt");
if (filePath !== null) {
    var doc = app.documents.add();
    var pageWidth = 11 * 72; // 11 inches
    var pageHeight = 8.5 * 72; // 8.5 inches

    // Set up document preferences
    doc.documentPreferences.pageWidth = pageWidth;
    doc.documentPreferences.pageHeight = pageHeight;
    doc.documentPreferences.facingPages = false;

    // Set margins
    var insideMargin = 0.5 * 72; // 0.5 inch
    var outsideMargin = 0.25 * 72; // 0.25 inch
    doc.marginPreferences.top = insideMargin;
    doc.marginPreferences.bottom = insideMargin;
    doc.marginPreferences.left = insideMargin;
    doc.marginPreferences.right = outsideMargin;

    var content = readFile(filePath).split('\n');
    var paragraphsPerPage = 4;
    var verticalSpacing = (pageHeight - (insideMargin * 2)) / paragraphsPerPage;

    for (var i = 0; i < content.length; i++) {
        if (i % paragraphsPerPage === 0 && i !== 0) {
            doc.pages.add();
        }

        var currentPage = doc.pages.item(Math.floor(i / paragraphsPerPage));
        var position = [
            insideMargin + (i % paragraphsPerPage) * verticalSpacing,
            insideMargin,
            insideMargin + ((i % paragraphsPerPage) + 1) * verticalSpacing,
            pageWidth - outsideMargin
        ];

        createTextFrame(currentPage, content[i], (i + 1).toString(), position);
    }
}
