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
function createTextFrame(page, content, number, topPosition, arialFont, pageWidth, leftMargin, rightMargin) {
    var textFrame = page.textFrames.add();
    var frameHeight = 72; // Height of each text frame in points
    var frameWidth = pageWidth - leftMargin - rightMargin; // Width of each text frame considering margins

    textFrame.geometricBounds = [topPosition, leftMargin, topPosition + frameHeight, leftMargin + frameWidth];
    textFrame.contents = number + ' ' + content;

    // Center the text frame content
    textFrame.textFramePreferences.verticalJustification = VerticalJustification.CENTER_ALIGN;

    // Apply paragraph style to make the number large and add space between lines
    var paragraph = textFrame.paragraphs.item(0);
    var firstWord = paragraph.words.item(0);
    firstWord.pointSize = 48; // Adjust the size as needed
    firstWord.fontStyle = "Bold"; // Make the number bold

    // Apply paragraph alignment and set font and leading
    paragraph.justification = Justification.CENTER_ALIGN;
    paragraph.leading = 100; // Add extra space between lines
    paragraph.appliedFont = arialFont;
    paragraph.pointSize = 48;
}

// Main Script
var filePath = File.openDialog("Select your text file", "*.txt");
if (filePath !== null) {
    var doc = app.documents.add();
    var pageWidth = 11 * 72; // 11 inches
    var pageHeight = 8.5 * 72; // 8.5 inches

    // Set up document preferences
    with (doc.documentPreferences) {
        pageWidth = 11 * 72; // 11 inches
        pageHeight = 8.5 * 72; // 8.5 inches
        facingPages = false;
    }

    // Set margins
    var topMargin = 0.5 * 72; // 0.5 inch
    var bottomMargin = 0.5 * 72; // 0.5 inch
    var leftMargin = 0.5 * 72; // 0.5 inch
    var rightMargin = 0.25 * 72; // 0.25 inch
    with (doc.marginPreferences) {
        top = topMargin;
        bottom = bottomMargin;
        left = leftMargin;
        right = rightMargin;
    }

    // Set default language to English
    doc.textDefaults.appliedLanguage = "English: USA";

    var content = readFile(filePath).split('\n');
    var paragraphsPerPage = 4;
    var verticalSpacing = (pageHeight - topMargin - bottomMargin) / paragraphsPerPage;

    // Set default Arial font
    var arialFont = "Arial";

    for (var i = 0; i < content.length; i++) {
        if (i % paragraphsPerPage === 0 && i !== 0) {
            doc.pages.add();
        }

        var currentPage = doc.pages.item(Math.floor(i / paragraphsPerPage));
        var topPosition = topMargin + (i % paragraphsPerPage) * verticalSpacing;

        createTextFrame(currentPage, content[i], (i + 1).toString(), topPosition, arialFont, pageWidth, leftMargin, rightMargin);
    }
}
