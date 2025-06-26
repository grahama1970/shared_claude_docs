# DARPA ACERT/SpartaAI Presentations Summary

## Document 1: ACERT_Darpa_PI_Meeting_FtWorth_NoBrandonVideo.pptx

### Overview
- **Event**: DARPA PI Meeting, Fort Worth
- **Focus**: ACERT (Automated Cyber Evaluation of Requirements and Threats)
- **Key Presenters**: Graham (indicated by 'G' markers)

### Main Sections

#### 1. ACERT Overview (Slides 1-12)
**Core Purpose**: 
- Takes "horrible-pointless-rote grunt work" out of extracting requirements
- Converts messy documentation into queryable datasets
- Process 1,000+ page documents in ~1 minute

**Technical Pipeline**:
1. Extract from datalake
2. Extract sections
3. Extract data from sections
4. Multi-pass lexical encode/word embed
5. Clause logic/temporal logic extraction
6. Confidence tests

**Key Capabilities**:
- Requirements extraction with confidence scores (32%-96%)
- Requirement-Based Coverage
- Linkages through attributes
- Tables and Code deconstruction
- Images to Text conversion

**Supported Actions**:
- Track Variable States
- Assess/Verify Linkages
- Find Requirement Collisions and Duplications
- Create Cascading Error Scenarios
- Export to: PyfoRel (ASU), GE SADL, Honeywell CLEAR, Sandia QSpec

#### 2. Auto-Map Security Controls (Phase 3-4)
**Vision**: Non-domain experts can map requirements to:
- NIST Controls
- CFS Tools
- SPARTA (threats, countermeasures)
- MITRE ATT&CK

**Auto-Rating**: Projects can be rated from "script kiddie to state actor" threat level

#### 3. Accomplishments (Slide 13)
**Extraction Results**:
- 3,015 requirements extracted from UPSAT datalake
- Image-to-text conversion (inline with table data)
- Word embeddings for similarity analysis
- Units, Acronyms, Definitions, Operators, Entities extraction

**Technical Improvements**:
- Optimized for LLM queries
- Code simplified and optimized
- Dynamic and Static Swapping
- NLP Engine refactored

#### 4. CHSS Integration (Slides 15-19)
**GitHub Ticket Analysis**:
- Extract meaningful assurance information from tickets
- Match to SPARTA, NIST, and MITRE resources
- Feed into Arbiter for formal verification

**Example Ticket Analyzed**:
- Title: "Intermittent Data Corruption in Satellite's Telemetry Communication Module"
- Issue: 1 in 10 telemetry messages corrupted
- Goal: Extract engineering patterns and map to threats/countermeasures

---

## Document 2: ACERT_PI_Meeting_Mar_12_DEMO_NY_Grammatech_v2.pptx

### Overview
- **Event**: DARPA PI Meeting, New York (March 12)
- **Focus**: SpartaAI - Evolution of ACERT with AI integration
- **Collaboration**: GrammaTech demonstration

### Main Sections

#### 1. SpartaAI Value Proposition (Slides 1-4)
**Core Message**: 
"SpartaAI uses modern AI and formal methods techniques to extract, debug, and formalize tedious requirement into threat maps while deferring complicated requirements to the human"

**Problems Addressed**:
- Manual threat mapping is insufficient
- Tedious and labor intensive
- Requires embedded cybersecurity experts (scarce resource)
- Human negative bias wastes resources on unlikely catastrophic scenarios

**Solution**:
- Combine AI techniques (LLMs, NLP, ML) with SPARTA knowledge
- Transform SPARTA from reference to automated assistant

#### 2. SpartaAI Vision (Slides 5-7)
**9-Month Goals**:
- Limit reliance on cybersecurity experts
- Make SPARTA queryable by non-experts
- Automated mapping of requirements to threats
- Integrate cybersecurity early in product lifecycle

**Implementation**:
- Queryable LLM with expert system hooks
- Local deployment on Horus workstation (ITAR-compliant)
- Optional cloud deployment (AWS GovCloud)

**Vision Demo**:
- User asks: "What are the most catastrophic threats for id 18?"
- System responds with ordered threats
- Auto-populates TTPs in system model framework
- Provides project threat rating (e.g., "State Actor")

#### 3. ACERT Deep Dive (Slides 8-14)
**Origin Story**:
- 4-year DARPA collaboration
- 16+ teams across Military-Industrial Complex
- Tech transferred to Aerospace (SpartaAI) and CHSS/ARCOS

**Problem-Solution Math**:
- Single engine: 10,000+ requirements
- Each requirement: ~8 hours to breakdown
- Total: 80,000 hours
- Goal: Save 15% through intelligent automation

**Technical Process** (Enhanced from v1):
1. Extract from datalake
2. Extract sections
3. Extract data from sections
4. Multi-pass lexical/ML encode
5. Clause logic and variable/temporal logic extraction
6. Confidence tests

**Journey Example**:
Shows requirement extraction with confidence scores:
- "When X is False, the SP shall activate X Thing 2" (96% confidence)
- "Upon power-up, after an EGI encounters a pizza interrupt..." (32% confidence)

### Key Differences Between Presentations

1. **Evolution**: Fort Worth focused on ACERT core, NY showed SpartaAI AI integration
2. **Scope**: Expanded from extraction to threat mapping with LLMs
3. **Deployment**: Added ITAR-compliant local workstation emphasis
4. **Automation Level**: Moved from "save 15% time" to "non-experts can do expert work"

### Critical Technical Details

**File Types Supported**:
- docx, pdf, md, xml, text, excel
- Multiple requirement documentation types
- Subsections and recommendations

**Integration Points**:
- Boeing artifacts via datalake
- RACK API for team collaboration
- GE STR teams integration

**Performance Metrics**:
- 1,000+ pages in ~1 minute
- Confidence scores from 32% to 96%
- 3,015 requirements extracted from UPSAT

### Key Phrases/Concepts to Remember

1. "Horrible-pointless-rote grunt work" - The problem ACERT solves
2. "Machines handle rote/easy, Humans handle complicated/nuanced"
3. "Script kiddie to state actor" - Threat rating scale
4. "Pizza interrupt" - Example of quirky requirement language
5. "Negative bias" - Human tendency to focus on unlikely catastrophic scenarios
6. "ITAR-compliant" - Critical for defense applications
7. "Horus workstation" - Local deployment platform

### SPARTA Integration Details
- Threats and countermeasures database
- CWE mappings
- Automated threat ordering by severity
- Integration with system modeling frameworks

This summary captures the essential information from both presentations for future reference and comparison with GRANGER's evolution.
