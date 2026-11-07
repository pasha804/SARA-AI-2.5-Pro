# Graph Report - MARAA AI  (2026-11-08)

## Corpus Check
- Large corpus: 231 files · ~3,251,234 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder.

## Summary
- 1984 nodes · 3485 edges · 186 communities (37 shown, 149 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 126 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 8
- Community 9
- Community 10
- Community 11
- Community 12
- Community 13
- Community 14
- Community 15
- Community 16
- Community 17
- Community 18
- Community 19
- Community 21
- Community 22
- Community 23
- Community 24
- Community 25
- Community 26
- Community 27
- Community 28
- Community 29
- Community 30
- Community 31
- Community 32
- Community 33
- Community 34
- Community 35
- Community 36
- Community 37
- Community 38
- Community 39
- Community 40
- Community 41
- Community 42
- Community 43
- Community 44
- Community 45
- Community 46
- Community 47
- Community 48
- Community 49
- Community 50
- Community 51
- Community 52
- Community 53
- Community 54
- Community 55
- Community 56
- Community 57
- Community 58
- Community 59
- Community 60
- Community 61
- Community 62
- Community 63
- Community 64
- Community 65
- Community 66
- Community 67
- Community 68
- Community 69
- Community 70
- Community 71
- Community 72
- Community 73
- Community 74
- Community 75
- Community 76
- Community 77
- Community 78
- Community 79
- Community 80
- Community 81
- Community 82
- Community 83
- Community 84
- Community 85
- Community 86
- Community 88
- Community 89
- Community 90
- Community 91
- Community 92
- Community 93
- Community 94
- Community 95
- Community 96
- Community 97
- Community 98
- Community 99
- Community 100
- Community 101
- Community 102
- Community 103
- Community 105
- Community 106
- Community 107
- Community 108
- Community 109
- Community 110
- Community 111
- Community 112
- Community 113

## God Nodes (most connected - your core abstractions)
1. `TestAll120ToolsLive` - 123 edges
2. `record_tool_audit()` - 121 edges
3. `TestSARAAllToolsExhaustive` - 74 edges
4. `startServer()` - 37 edges
5. `CognitiveRuntime` - 28 edges
6. `AutonomousMind` - 27 edges
7. `DiscordAutonomousManager` - 18 edges
8. `DiscordAutonomousManager` - 18 edges
9. `SaraInteractiveBrowserAgent` - 18 edges
10. `ApiCapabilityRegistry` - 17 edges

## Surprising Connections (you probably didn't know these)
- `TestAdvancedFeatures` --uses--> `BrowserDeepDive`  [INFERRED]
  tests/test_advanced_features.py → SARA/resources/app/sara_browser_deepdive.py
- `TestTaskManagerAndHF` --uses--> `HuggingFaceProvider`  [INFERRED]
  tests/test_task_manager_and_hf.py → SARA/resources/app/sara_hf_provider.py
- `TestTaskManagerAndHF` --uses--> `BackgroundTaskManager`  [INFERRED]
  tests/test_task_manager_and_hf.py → SARA/resources/app/sara_task_manager.py
- `TestAdvancedFeatures` --uses--> `SaraWakeWordDetector`  [INFERRED]
  tests/test_advanced_features.py → SARA/resources/app/sara_wakeword.py
- `TestAdvancedFeatures` --uses--> `WhatsAppVoiceTranscriber`  [INFERRED]
  tests/test_advanced_features.py → SARA/resources/app/sara_whatsapp_voice.py

## Import Cycles
- None detected.

## Communities (186 total, 149 thin omitted)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (46): AdapterExecutionOptions, clamp(), executeVerifiedAdapter(), fetchWithSafeRedirects(), normalizeParameters(), readRestrictedJsonPath(), redactUrl(), renderPath() (+38 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (3): AntigravityBridge, AntigravityBridge, TestAntigravityBridge

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (6): browser_search_and_click(), build_and_launch_project(), capture_webcam_frame(), create_2d_car_game_project(), research_topic_intelligence(), verify_ai_model_or_tech()

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (20): CognitionConfig, CognitiveRuntimeOptions, ConfirmationStore, PendingConfirmation, SafetyAssessment, SafetyPolicy, result(), ToolExecutor (+12 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (18): AttentionEngine, loadCognitionConfig(), number(), InitiativeEngine, reasonFor(), toneFor(), CognitionOutcome, CognitiveRuntime (+10 more)

### Community 6 - "Community 6"
Cohesion: 0.07
Nodes (39): dotenv, express, @google/genai, lucide-react, mmd-parser, motion, react, react-dom (+31 more)

### Community 8 - "Community 8"
Cohesion: 0.07
Nodes (5): DeepResearchCrawler, EmailNotificationDigest, SocialMediaDiscordPublisher, StudyNotesAndPdfTutor, WhatsAppSmartPipeline

### Community 9 - "Community 9"
Cohesion: 0.06
Nodes (6): add_halo_to_pmx(), generate_royal_cobalt_lining(), generate_silky_hair_pattern(), process_textures(), lengthen_hair(), sculpt_and_style_model()

### Community 10 - "Community 10"
Cohesion: 0.09
Nodes (5): AutonomousMind, eventTypeFor(), reasonForOrigin(), thoughtPriority(), ConversationContinuationEngine

### Community 11 - "Community 11"
Cohesion: 0.09
Nodes (24): activeScreenVisionPipelines, API_HUB_TOOLS, assertSafeExternalUrl(), collectNativeDesktopObservation(), createContextualThoughtCandidate(), DESKTOP_TOOLS, ElectronScreenCaptureResponse, ensureDesktopObserver() (+16 more)

### Community 12 - "Community 12"
Cohesion: 0.09
Nodes (3): ProjectManager, ProjectManager, TestProjectManager

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (5): get_all_models(), main(), test_single_model(), main(), test_model()

### Community 15 - "Community 15"
Cohesion: 0.11
Nodes (6): create_verified_dir(), create_verified_file(), format_tool_response(), open_path_verified(), resolve_user_path(), TestSaraReliability

### Community 17 - "Community 17"
Cohesion: 0.08
Nodes (10): run_browser_task(), analyze_whatsapp_chat(), browser_search_and_click(), build_and_launch_project(), capture_webcam_frame(), create_2d_car_game_project(), get_jarvis_intelligence_card(), research_topic_intelligence() (+2 more)

### Community 21 - "Community 21"
Cohesion: 0.09
Nodes (3): SelfImprovementEngine, SelfImprovementEngine, TestSelfImprovement

### Community 26 - "Community 26"
Cohesion: 0.18
Nodes (12): AddMemoryInput, clamp(), extractEntities(), inferProject(), legacyKind(), LegacyMemoryLike, MemoryFile, normalize() (+4 more)

### Community 27 - "Community 27"
Cohesion: 0.10
Nodes (3): AdvancedBrowserInteractionEngine, PowerPointPresentationEngine, WordDocumentAutomationEngine

### Community 28 - "Community 28"
Cohesion: 0.11
Nodes (18): buildInitiativePrompt(), classifyUserEventType(), isPauseAutonomyIntent(), isResumeAutonomyIntent(), isStopIntent(), isTalkNormallyIntent(), legacyCategoryForKind(), formatSystemInstructionsWithMemories() (+10 more)

### Community 29 - "Community 29"
Cohesion: 0.13
Nodes (5): create_verified_dir(), create_verified_file(), format_tool_response(), open_path_verified(), resolve_user_path()

### Community 31 - "Community 31"
Cohesion: 0.22
Nodes (7): clamp(), CreateGoalInput, deriveGoalStatus(), GoalFile, GoalManager, unique(), validateTaskGraph()

### Community 32 - "Community 32"
Cohesion: 0.15
Nodes (10): CacheEntry, loadModelRoutes(), ModelProvider, ModelRouter, ModelRouterOptions, clamp(), GoalPlanner, parseJson() (+2 more)

### Community 33 - "Community 33"
Cohesion: 0.15
Nodes (15): { app, BrowserWindow, Menu, shell, dialog, ipcMain, desktopCapturer, session, screen }, APP_ICON, bootstrap(), captureDisplayForBackend(), createMainWindow(), createSplashWindow(), debugLog(), fs (+7 more)

### Community 35 - "Community 35"
Cohesion: 0.16
Nodes (11): AutonomousMindOptions, clamp(), DeepThoughtGenerator, InternalThoughtContext, normalizeThought(), boundedUnique(), ContinuationOpportunity, inferTopic() (+3 more)

### Community 36 - "Community 36"
Cohesion: 0.12
Nodes (3): get_saved_contacts(), whatsapp_open_chat(), TestFullAutomationAndSkills

### Community 39 - "Community 39"
Cohesion: 0.17
Nodes (6): clamp(), inferInterruptionCost(), semanticKeyFor(), SocialDecision, SocialEvaluation, SocialInitiativeEngine

### Community 40 - "Community 40"
Cohesion: 0.23
Nodes (7): clamp(), LearnSkillInput, normalizeName(), sanitizeSteps(), SkillFile, SkillManager, unique()

### Community 41 - "Community 41"
Cohesion: 0.17
Nodes (11): executeNodeNativeTool(), clearGeminiApiKey(), DATA_DIR, getGeminiApiKey(), hasGeminiApiKey(), readSecrets(), Secrets, SECRETS_FILE (+3 more)

### Community 42 - "Community 42"
Cohesion: 0.17
Nodes (3): FirecrawlDeepKnowledgeCrawler, HeadroomContextBudgetGuard, VibeKanbanSprintAutomator

### Community 43 - "Community 43"
Cohesion: 0.22
Nodes (3): ClaudeCodeRouterEngine, TasteSkillAestheticLinter, TestViralAutomationsPart2

### Community 45 - "Community 45"
Cohesion: 0.22
Nodes (5): DesktopDownloadSnapshot, DesktopPerception, DesktopPerceptionOptions, DesktopSnapshot, downloadKey()

### Community 46 - "Community 46"
Cohesion: 0.17
Nodes (4): PRIORITY, SpeechOrchestrator, SpeechRequest, SpeechSource

### Community 52 - "Community 52"
Cohesion: 0.24
Nodes (11): appendLog(), callDesktopAgent(), captureViaElectron(), ensureDesktopAgent(), fetchAgentToolCount(), isDesktopAgentAlive(), logCommand(), logError() (+3 more)

### Community 53 - "Community 53"
Cohesion: 0.18
Nodes (10): author, description, license, main, name, scripts, dev, start (+2 more)

### Community 54 - "Community 54"
Cohesion: 0.18
Nodes (10): author, description, license, main, name, scripts, dev, start (+2 more)

### Community 57 - "Community 57"
Cohesion: 0.36
Nodes (8): clamp(), defaultSignals(), deriveSemanticKey(), explain(), inferInterruptionCost(), lowSignalObservation(), SeenEvent, signal()

### Community 58 - "Community 58"
Cohesion: 0.24
Nodes (3): clamp(), CognitiveEventBus, EventListener

### Community 73 - "Community 73"
Cohesion: 0.39
Nodes (5): createCompanionDashboard(), createHudElement(), createTaskDashboardElement(), initAll(), setupModalObserver()

## Knowledge Gaps
- **149 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TestSARAAllToolsExhaustive` connect `Community 38` to `Community 128`, `Community 129`, `Community 130`, `Community 131`, `Community 132`, `Community 133`, `Community 134`, `Community 135`, `Community 136`, `Community 137`, `Community 138`, `Community 139`, `Community 140`, `Community 141`, `Community 142`, `Community 143`, `Community 144`, `Community 145`, `Community 146`, `Community 147`, `Community 148`, `Community 149`, `Community 150`, `Community 151`, `Community 152`, `Community 25`, `Community 153`, `Community 154`, `Community 155`, `Community 156`, `Community 157`, `Community 158`, `Community 159`, `Community 160`, `Community 161`, `Community 162`, `Community 36`, `Community 163`, `Community 164`, `Community 165`, `Community 166`, `Community 167`, `Community 168`, `Community 169`, `Community 172`, `Community 173`, `Community 174`, `Community 175`, `Community 176`, `Community 170`, `Community 171`, `Community 114`, `Community 115`, `Community 116`, `Community 117`, `Community 118`, `Community 119`, `Community 120`, `Community 121`, `Community 122`, `Community 123`, `Community 124`, `Community 125`, `Community 126`, `Community 127`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.03359858532272325 - nodes in this community are weakly interconnected._
- **Why does `TestAll120ToolsLive` connect `Community 0` to `Community 3`, `Community 36`, `Community 103`, `Community 108`, `Community 109`, `Community 113`, `Community 25`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.05583308845136644 - nodes in this community are weakly interconnected._
- **Why does `record_tool_audit()` connect `Community 0` to `Community 3`, `Community 36`, `Community 103`, `Community 108`, `Community 109`, `Community 113`, `Community 25`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.05142857142857143 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.07536231884057971 - nodes in this community are weakly interconnected._