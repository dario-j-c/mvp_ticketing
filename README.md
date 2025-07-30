# S.E. Team Interim Ticketing System

## Request Documentation & Workflow Guide

-----

## How to Use This Document

**For Requesting Parties (e.g., Conservation, Operations, etc.):**

Use this template to clearly communicate:

  - issues,
  - requests, and
  - tasks to the S.E. team.

Complete **all** relevant sections to ensure your needs are understood and properly prioritized.

Providing thorough details helps the S.E. team address your request efficiently and accurately.

**For S.E. Team Members:**

This document aims to provide complete context for each request, including:

  - business impact,
  - technical requirements, and
  - success criteria.

Use it to understand priorities and delivery expectations.

The detailed information within each ticket will help minimize the need for back-and-forth clarification, allowing you to focus on effective solutions.

**For Both Parties:**

This serves as our validation and communication bridge *until a permanent ticketing system is implemented*.

Each completed ticket represents a **mutual agreement** on:

  - scope,
  - priority, and
  - expectations.

This assumes a discussion is held where any ticket is validated, or can be considered validated.

*The act of collaboratively filling out and reviewing these tickets can serve as a structured conversation, ensuring both parties are aligned even without a direct, real-time dialogue.*

-----

## Ticket Types & When to Use Them

### Bug Report - *Something is broken or not working as expected*

  - System errors, crashes, or unexpected behavior
  - Features that don't work as designed
  - Performance issues affecting daily work

### Feature Request - *New functionality or improvements*

  - New capabilities needed for your work
  - Enhancements to existing features
  - User experience improvements

### Task - *General work items or maintenance*

  - Data updates or content changes
  - Documentation requests
  - System maintenance or configuration changes

-----

## Ticket Template

### Basic Information

```
Ticket ID: [Auto-assigned by S.E. team]
Date Created: [DD-MMM-YYYY]
Current Status: [Staging]
Priority: [Critical/High/Medium/Low]
```

### Reporter Information

```
Name: [Your full name]
User Group: [QA / Conservator / Sys Admin / Other]
Contact: [Email/Extension for follow-up]
Department/Project: [Which area of work this affects]
```

-----

## BUG REPORT TEMPLATE

### Title

*Brief, descriptive summary of the issue*

```
Example: "Database search returns no results for objects with special characters"
```

### Category

  - [ ] Error Page (System shows error message)
  - [ ] Unexpected Behaviour (System does something wrong)
  - [ ] Perceived Lag (System is too slow)
  - [ ] Data Issue (Information is incorrect/missing)
  - [ ] Access Issue (Cannot reach or use feature)

### Link/Location

```
URL where issue occurs: [Full URL]
Page/Section: [Specific area of the system]
Browser/Device: [Chrome, Firefox, Mobile, etc.]
```

### Steps to Reproduce

*Detailed steps so S.E. team can recreate the issue. Clarity here is key to avoiding assumptions and ensuring accurate diagnosis.*

```
1. Go to [specific page]
2. Click on [specific button/link]
3. Enter [specific data]
4. Observe [what happens]
```

### Expected vs Actual Results

```
Expected: [What should happen. Describe the ideal outcome.]
Actual: [What actually happens. Describe the current, problematic outcome.]
```

### Screenshots/Evidence

*Attach screenshots, error messages, or relevant files. Visual evidence can significantly reduce misinterpretations.*

```
[Attach files or describe visual evidence]
```

### Impact Assessment

  - [ ] **Critical** - Blocks essential work, affects multiple users, high business risk.
  - [ ] **High** - Significant impact on daily operations, critical functionality impaired.
  - [ ] **Medium** - Workaround available, but inconvenient or inefficient.
  - [ ] **Low** - Minor issue, minimal impact, cosmetic.

### Business Context

*Help S.E. understand why this matters. This section is crucial for prioritizing and understanding the real-world implications of the bug. It provides the "why" behind the fix.*

```
Who is affected: [Number of users, which departments (e.g., Conservation, Finance)]
Work impact: [How this affects daily operations, workflows, or data integrity for the affected group]
Urgency: [Any time-sensitive factors or upcoming deadlines this impacts]
```

-----

## FEATURE REQUEST TEMPLATE

### Title

*Clear description of the desired functionality*

```
Example: "Add bulk export feature for condition reports"
```

### Category

  - [ ] Aesthetic (Visual improvements, UI changes)
  - [ ] Functionality (New capabilities or workflow improvements)

### Current Situation

*What exists now and what's missing. Explaining the current process helps the S.E. team understand the problem you're trying to solve, not just the solution you envision.*

```
Current process: [How you do this work now, step-by-step]
Limitations: [What's difficult, inefficient, or impossible with the current process]
```

### Desired Functionality

*Detailed description of what you want. Think about the user experience and the specific actions you envision.*

```
User story: "As a [role, e.g., Conservator], I want to [action] so that [benefit]"

Specific requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]
```

### Success Criteria

*How will we know this feature is working correctly? Defining success upfront ensures alignment and clarity on delivery. This also provides objective benchmarks for testing and acceptance.*

```
Definition of done:
- [ ] [Specific outcome 1 (e.g., "All condition reports can be exported to CSV")]
- [ ] [Specific outcome 2 (e.g., "Export includes all relevant data fields")]
- [ ] [Specific outcome 3 (e.g., "Export process completes within 30 seconds for 1000 records")]

Testing scenarios:
- Test with [specific data/situation, e.g., "Test with a dataset containing special characters"]
- Verify [specific behavior, e.g., "Verify that all selected records are included in the export"]
```

### Business Value

*Quantify the benefit. This helps the S.E. team understand the strategic importance and can inform prioritization.*

```
Time savings: [How much time this saves daily/weekly for specific roles or teams]
Quality improvement: [How this improves the accuracy, consistency, or reliability of work]
User benefit: [How many people this helps and in what specific ways]
Strategic importance: [How this supports larger organizational goals or initiatives]
```

### Needed Requirements *(Internal S.E. Section)*

*Steps that must occur before implementation*

```
- [ ] Requirements analysis
- [ ] Design review with stakeholders
- [ ] Data model changes
- [ ] Integration considerations
- [ ] Testing strategy
```

### Related Systems/Dependencies

```
Existing features that connect: [List related functionality within current systems]
External systems involved: [APIs, databases, third-party tools]
Data requirements: [What information is needed for this feature to function]
```

-----

## TASK TEMPLATE

### Title

*Brief description of the work needed*

```
Example: "Update user permissions for new Conservation staff"
```

### Task Type

  - [ ] Data Update (Content changes, information updates)
  - [ ] Configuration (Settings, permissions, system setup)
  - [ ] Documentation (Guides, procedures, help content)
  - [ ] Maintenance (Routine system upkeep)
  - [ ] Research (Investigation or analysis needed)

### Detailed Description

*Complete explanation of what needs to be done. Provide enough detail for the S.E. team to execute without further questions.*

```
Background: [Why this task is needed. Provide context for the request.]
Specific work: [Exactly what should be done, step-by-step if applicable.]
Expected outcome: [What the result should be once the task is complete.]
```

### Requirements & Constraints

```
Access needed: [Special permissions or systems required to complete this task]
Timeline: [When this needs to be completed, if there's a deadline]
Dependencies: [What must happen first or what other tasks this relies on]
Special considerations: [Important factors to consider, e.g., data sensitivity, specific formatting]
```

### Acceptance Criteria

```
Task is complete when:
- [ ] [Specific deliverable 1, e.g., "New Conservation staff have correct access roles confirmed"]
- [ ] [Specific deliverable 2, e.g., "Configuration changes are documented"]
- [ ] [Verification step completed, e.g., "Able to log in and access specified modules"]
```

-----

## Workflow Stages & What They Mean

### Staging

  - Newly submitted ticket
  - Initial review by S.E. team [or chosen delegate(s)]
  - May require clarification or additional information to proceed. This stage allows for initial alignment before deeper work begins.

### Accepted/Validated

  - Requirements confirmed and understood
  - Technical approach determined
  - Scheduled for development
  - **Mutual agreement**: Scope and expectations are clear. This is a crucial handshake moment, signifying both teams agree on what needs to be done and how success will be measured.

### In Progress

  - Active development or work underway
  - Regular updates provided
  - May involve testing or feedback cycles.

### Completed

  - Work finished and deployed/delivered
  - Ready for user acceptance testing
  - Documentation updated if needed.

### Rejected

  - Cannot be implemented as requested
  - Detailed explanation provided
  - Alternative solutions may be suggested. This provides a clear "no" with reasoning, which is important for understanding limitations and exploring other avenues.

### Frozen

  - Work paused due to dependencies or priorities
  - Will be reconsidered when conditions change
  - Clear timeline or conditions for resumption provided. This prevents tickets from being forgotten and ensures transparency about delays.

-----

## Timeline Expectations (TO BE DISCUSSED)

*The following estimates **are not** guarantees or in any way indicative of actual timelines. These will vary based on current workload, complexity, and dependencies. Transparent communication around these estimates helps manage expectations.*

### Response Times

  - **Initial acknowledgment**: 1 business day
  - **Status update**: 2-3 business days
  - **Validation/Requirements clarification**: 3-5 business days

### Development Timelines *(Estimates)*

  - **Bug fixes**: 1-5 business days depending on complexity
  - **Small features**: 1-2 weeks
  - **Medium features**: 2-4 weeks
  - **Large features**: 4-8 weeks
  - **Tasks**: 1-3 business days

*Note: Timelines vary based on current workload, complexity, and dependencies. Transparent communication around these estimates helps manage expectations.*

### Priority Guidelines (TO BE DISCUSSED)

  - **Critical**: Response within 4 hours, resolution within 24 hours (e.g., production system down)
  - **High**: Response within 1 day, resolution within 1 week (e.g., significant workflow disruption)
  - **Medium**: Response within 2 days, resolution within 2-3 weeks (e.g., minor efficiency improvements)
  - **Low**: Response within 3 days, resolution as capacity allows (e.g., cosmetic changes, minor tasks)

-----

## Communication & Updates (TO BE DISCUSSED)

### Status Updates

  - S.E. team provides updates every Friday (*choose an appropriate day*)  on all active tickets.
  - Significant changes (e.g., unexpected blockers, major scope changes) communicated immediately.
  - Blocked items escalated within 24 hours to ensure quick resolution and transparency.

### Clarification Process

1.  S.E. team may request additional information to ensure full understanding of the request.
2.  The requesting party (e.g., Conservation) provides details within 2 business days to keep the process moving.
3.  Ticket moves to "Accepted/Validated" once all necessary information is clear and agreed upon. This iterative process, done through the ticket itself, can reduce the need for direct conversations that might be difficult.

### Testing & Feedback

  - Features delivered to staging environment first for review.
  - Requesting party (e.g., Conservation) tests and provides feedback. **Thorough testing from your end is critical for ensuring the solution meets your needs.**
  - Issues identified during testing are resolved before production deployment.

### Change Requests

  - Scope changes require a new ticket or an amendment to the current one.
  - Impact on timeline and effort will be communicated clearly.
  - Mutual agreement is required for any major changes to ensure both parties are aligned. This structured approach to changes can prevent misunderstandings and scope creep.

-----

## Internal S.E. Team Section

### Technical Assessment *(For S.E. Team Use)*

```
Complexity: [Low/Medium/High/Very High]
Estimated effort: [Hours/Days/Weeks]
Technical approach: [Brief description of how the task will be executed]
Risks/Concerns: [Potential issues or challenges during implementation]
Dependencies: [What internal or external factors this work relies on]
```

### Progress Tracking

```
Start date: [DD-MMM-YYYY]
Target completion: [DD-MMM-YYYY]
Current progress: [% complete or milestone reached]
Blockers: [What's preventing progress, and what's needed to resolve it]
Next steps: [What happens next in the development cycle]
```

### Testing Notes

```
Test cases: [Key scenarios to verify functionality and ensure quality]
Test data needed: [Special requirements for testing environments]
Known issues: [Current limitations or workarounds within the implemented solution]
Deployment notes: [Special considerations for moving to production]
```

-----

## Quick Reference & Tips

### For Requesting Parties (e.g., Conservation)

  - **Be specific**: More detail leads to better solutions and fewer misunderstandings.
  - **Include context**: Help the S.E. team understand the "why" behind your request – the real problem it solves.
  - **Provide examples**: Real scenarios, data, or screenshots help design and troubleshoot more effectively.
  - **Test thoroughly**: Try edge cases and unusual situations when a solution is delivered for testing.

### For S.E. Team

  - **Ask clarifying questions**: Don't assume requirements; use the ticket to ask for more detail.
  - **Communicate progress**: Keep stakeholders informed, even with small updates, to build trust.
  - **Document decisions**: Record rationale for future reference and to maintain institutional knowledge.
  - **Test from user perspective**: Verify that the solution actually improves the user's workflow.

### Common Pitfalls to Avoid

  - ❌ Vague descriptions ("Make it better")
  - ❌ Missing business context ("Just fix it")
  - ❌ Unrealistic timelines ("Need it yesterday")
  - ❌ Scope creep without discussion
  - ❌ Skipping testing or validation

-----

## Escalation & Support

### When to Escalate

  - Critical system outages that halt operations.
  - Missed deadlines affecting core business functions.
  - Unclear requirements after multiple attempts at clarification within the ticket.
  - Resource conflicts or priority disputes that cannot be resolved directly between teams.

### Escalation Process

1.  Direct discussion between teams' primary contacts, utilizing the ticket as a basis for the conversation.
2.  Involvement of department managers from both sides to facilitate resolution.
3.  Senior leadership review if needed, for high-impact or persistent issues.

### Emergency Contact

```
Critical issues outside business hours:
[Contact information for emergency support]
```

-----

*This document will be replaced by our permanent ticketing system once implemented. All current tickets will be migrated to ensure continuity.*

**Document Version**: 0.1
**Last Updated**: [29-Jul-2025]
**Next Review**: [Date + 30 days]
