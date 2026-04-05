# 🧩 AI Requirement Helper

An intelligent AI-powered tool that transforms requirements into structured documentation. Get smart summaries, acceptance criteria, and test cases generated in seconds using Google Gemini AI.

## ✨ Features

- 🤖 **AI-Powered Generation** - Uses Google Gemini to generate contextual acceptance criteria and test cases
- 📝 **Smart Summarization** - Creates concise, professional summaries of requirements
- ✅ **Acceptance Criteria** - Generates 5+ relevant acceptance criteria specific to your requirement
- 🧪 **Test Cases** - Produces practical, context-aware test scenarios
- 📜 **History Tracking** - Keep a session history of all generated requirements with expandable details
- 🔗 **Traceability** - Includes type, priority, and generation date for compliance tracking
- 📥 **Export** - Download results as formatted text files
- 🎯 **Smart Detection** - Automatically detects requirement types (Authentication, File Handling, Data Processing, etc.)

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker (optional, for containerized deployment)
- Google Gemini API Key (free tier available at [ai.google.dev](https://ai.google.dev))

### Local Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-requirement-helper
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file in project root
   echo GEMINI_API_KEY=your_api_key_here > .env
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```

The app will open at `http://localhost:8501`

### Docker Installation

1. **Build the Docker image**
   ```bash
   docker build -t ai-requirement-helper .
   ```

2. **Run the container**
   ```bash
   docker run -p 8501:8501 ai-requirement-helper
   ```

3. **Access the app**
   Open `http://localhost:8501`

## 💡 How to Use

### Basic Workflow

1. **Enter your requirement** in the text area
   - Example: "Create a login system with password reset"
   - Be specific for better AI results

2. **Select priority level** (Low, Medium, High)

3. **Click "Generate"** button

4. **Review results:**
   - Requirement Type (Auto-detected)
   - Summary (AI-generated overview)
   - Acceptance Criteria (5+ items)
   - Test Cases (Practical scenarios)
   - Traceability Note (Type, Priority, Date)

5. **Export** results as text file if needed

6. **View history** to see all previous requirements

### Example Inputs

**Authentication:**
- "Users should be able to register a new account with email verification"
- "Implement two-factor authentication for user login"

**File Handling:**
- "Allow users to upload images and automatically create thumbnails"
- "Implement a document scanner that extracts text from PDF files"

**Data Processing:**
- "Generate a monthly sales report with filters for date range and product category"
- "Create a data export function that allows users to download their personal information"

**Search/Filter:**
- "Implement advanced search with filters for price, rating, and category"
- "Build real-time autocomplete search for user names"

## 🏗️ Project Structure

```
ai-requirement-helper/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (not in git)
├── Dockerfile            # Docker configuration
├── .dockerignore         # Docker ignore patterns
├── README.md             # This file
└── .git/                 # Git repository
```

## 🔧 Dependencies

- **streamlit** - Web framework for the UI
- **google-generativeai** - Google Gemini API client
- **python-dotenv** - Environment variable management

## 🤖 AI Generation Details

The app uses **Google Gemini API** to:
1. Analyze your requirement text
2. Detect the type of requirement (Authentication, File Handling, etc.)
3. Generate contextual acceptance criteria
4. Create practical test cases specific to the requirement
5. Produce professional summaries

If AI generation fails, the app automatically falls back to rule-based generation.

## 📋 Output Sections

### Requirement Type
Auto-detected category:
- Authentication
- File Handling
- Data Processing
- Search/Filter
- General (default)

### Summary
Professional 2-3 sentence overview including requirement focus, type, and priority.

### Acceptance Criteria
5-8 SMART criteria covering:
- Feature functionality
- Error handling
- Security considerations
- User feedback
- Data integrity (where applicable)

### Test Cases
5+ practical test scenarios covering:
- Valid input testing
- Invalid/edge cases
- Error scenarios
- Performance considerations
- Edge case handling

### Traceability Note
Compliance information including:
- Requirement type
- Priority level
- Generation date
- Link to testing artifacts

## 🔐 Security

- API key stored in `.env` (never committed to git)
- `.env` file excluded from Docker image by default
- No sensitive data logged or stored externally
- All processing done locally or via official Google APIs

## 🛠️ Troubleshooting

### Module Not Found Error
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### AI Generation Failed
The app will automatically use rule-based generation as fallback. Check:
- API key is valid in `.env`
- Google Gemini API free tier is active
- Internet connection is available

### Streamlit Port Already in Use
```bash
streamlit run app.py --server.port=8502
```

### Docker Build Failed
Ensure `.env` file exists and `.dockerignore` doesn't exclude it.

## 📊 Session Features

- **History Tracking** - All generated requirements saved in session
- **Expandable Details** - Click any history item to view full details
- **Clear History** - Remove all history with one click
- **Export** - Download any result as text file

## 🌟 Best Practices

1. **Be specific** in your requirements for better AI results
2. **Use industry terminology** when applicable
3. **Include context** about user roles or system constraints
4. **Specify acceptance criteria priorities** if needed
5. **Review and edit** generated content before use
6. **Export results** for documentation and tracking

## 📝 Example Requirement

**Input:**
```
Users should be able to upload PDF documents, validate them for required fields, and generate a summary report
```

**Generated Output:**
- **Type:** File Handling
- **Criteria:** Validation, format checking, user feedback, error handling, etc.
- **Test Cases:** Valid PDF upload, invalid format, missing fields, large files, etc.

## 🚀 Future Enhancements

- [ ] Support for multiple AI models (Claude, GPT-4)
- [ ] Batch requirement processing
- [ ] Custom criteria templates
- [ ] Integration with Jira/Azure DevOps
- [ ] PDF report export
- [ ] Collaborative editing features

## 📄 License

See LICENSE file for details.

## 🤝 Contributing

Contributions welcome! Please feel free to submit pull requests.

## 💬 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the example inputs
3. Ensure dependencies are installed
4. Verify API key is configured

---

**Made with ❤️ for better requirement management**
