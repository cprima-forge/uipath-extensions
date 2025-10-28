# UiPath SDK Extensions - Development Roadmap

**Current Version:** 0.0.5
**Last Updated:** 2025-10-26
**API Analysis:** Orchestrator v20.0 (339 endpoints)

## Executive Summary

The UiPath Python SDK covers approximately 15% of the Orchestrator API surface. This library bridges critical gaps through extension classes that wrap missing API functionality.

**Current Coverage:** ~25% (85+ operations across 11 extension classes)
**Remaining Gap:** ~75% (254+ endpoints across 90+ API families)

## What's Implemented (v0.0.5)

### Storage & Context Operations
- **ContextGroundingExt** - Storage bucket inspection, file listing, ingestion verification
- **BucketExtensions** - Direct bucket operations, file filtering, directory organization
- **FolderUtils** - Folder ID/Key conversion with caching

### Operations & Management
- **AssetsExt** - Complete asset CRUD, cross-folder operations, sharing
- **JobsExt** - Job listing, stop/restart, bulk operations, statistics
- **QueuesExt** - Queue definition management, retention policies, statistics
- **ProcessesExt** - Release version management, retention policies
- **SchedulesExt** - Time-based triggers (cron), schedule lifecycle
- **LibrariesExt** - Package management, version tracking, dependencies
- **TasksExt** - Human-in-the-loop workflows, form tasks, approvals
- **FolderManagementExt** - Folder CRUD, hierarchy navigation, permissions

**Total Methods:** 85+
**API Families Covered:** 11
**Production Ready:** Full type hints, error handling, caching, comprehensive documentation

## Phase 3 Priorities - TIER 1 Gaps

### 1. Test Automation (HIGHEST PRIORITY)

**Gap:** 29 endpoints, 0% SDK coverage
**Demand:** High - CI/CD automation, regression testing
**Complexity:** Medium

**Proposed Extension:** `TestAutomationExt`

**Core Methods:**
- `start_test_set_execution()` - Execute test set with options
- `cancel_test_execution()` - Stop running tests (test set or test case)
- `get_test_results()` - Retrieve test outcomes and metrics
- `list_test_sets()` - Get all test set definitions
- `list_test_executions()` - Get execution history
- `get_test_case_execution()` - Individual test case details
- `reexecute_failed_tests()` - Retry failures
- `get_test_attachments()` - Screenshots, logs, artifacts
- `manage_test_data_queue()` - Test data operations
- `create_test_set_for_release()` - Auto-generate test sets

**API Endpoints:**
- `/api/TestAutomation/StartTestSetExecution`
- `/api/TestAutomation/CancelTestSetExecution`
- `/api/TestAutomation/GetTestCaseExecutionAttachment`
- `/odata/TestSets`, `/odata/TestSetExecutions`
- `/odata/TestCaseDefinitions`, `/odata/TestCaseExecutions`
- `/odata/TestDataQueues`, `/odata/TestDataQueueItems`
- `/api/TestDataQueueActions/*` (7 endpoints)

**Use Cases:**
- Automated test orchestration in CI/CD pipelines
- Test result aggregation and reporting
- Regression testing automation
- Test data management
- Integration with test frameworks (pytest, unittest)

**Estimated Effort:** 2 weeks

---

### 2. Monitoring & Statistics

**Gap:** 16 endpoints, 0% SDK coverage
**Demand:** High - Operational dashboards, compliance, analytics
**Complexity:** Low (mostly read-only)

**Proposed Extension:** `MonitoringExt`

**Core Methods:**
- `get_entity_counts()` - Processes, assets, queues, robots counts
- `get_job_statistics()` - Success/failure/canceled aggregations
- `get_robot_statistics()` - Available/busy/disconnected counts
- `get_license_usage()` - Current license consumption
- `get_consumption_stats()` - Consumption-based licensing metrics
- `get_audit_logs()` - Security audit trail with filtering
- `export_audit_logs()` - CSV export for compliance
- `get_robot_logs()` - Execution logs with advanced filtering
- `get_session_statistics()` - Robot session metrics

**API Endpoints:**
- `/api/Stats/GetCountStats` - Entity counts
- `/api/Stats/GetJobsStats` - Job aggregations
- `/api/Stats/GetSessionsStats` - Robot stats
- `/api/Stats/GetLicenseStats` - License usage
- `/api/Stats/GetConsumptionLicenseStats` - Consumption metrics
- `/odata/AuditLogs`, `/odata/AuditLogs/.../Export`
- `/odata/RobotLogs`, `/odata/RobotLogs/.../GetFiltered`

**Use Cases:**
- Real-time operational dashboards
- License compliance tracking
- Cost allocation and chargeback
- Security audit compliance
- Performance analytics
- Capacity planning

**Estimated Effort:** 1 week

---

### 3. Robot Management

**Gap:** 21 endpoints, 0% SDK coverage
**Demand:** High - Robot fleet provisioning, health monitoring
**Complexity:** Medium

**Proposed Extension:** `RobotsExt`

**Core Methods:**
- `list_robots()` - Get all robots with filters
- `create_robot()` - Provision new robot
- `update_robot()` - Modify robot configuration
- `delete_robot()` - Decommission robot
- `get_robot_sessions()` - Active sessions
- `release_license()` - Free up runtime license
- `toggle_robot_state()` - Enable/disable robot
- `get_machine_mappings()` - Machine-to-license mappings
- `list_sessions()` - All robot sessions
- `get_global_sessions()` - Cross-folder session view

**API Endpoints:**
- `/odata/Robots` (12 endpoints)
- `/odata/Sessions` (9 endpoints)
- `/odata/Robots/UiPath.Server.Configuration.OData.ToggleEnabledState`
- `/odata/Sessions/UiPath.Server.Configuration.OData.ReleaseRuntimeLicense`

**Use Cases:**
- Robot fleet provisioning at scale
- Robot health monitoring
- Session management and cleanup
- License optimization
- Robot configuration automation

**Estimated Effort:** 1.5 weeks

---

## Phase 4 Priorities - TIER 2 Enhancements

### Completed Areas (Potential Enhancements)

**Assets (✅ v0.0.5)** - Consider adding:
- Bulk asset operations
- Asset templates
- Asset validation rules

**Jobs (✅ v0.0.5)** - Consider adding:
- Job priority management
- Job chaining/dependencies
- Advanced filtering by execution time

**Queues (✅ v0.0.5)** - Consider adding:
- Queue item bulk operations
- Queue SLA monitoring
- Queue performance metrics

**Processes (✅ v0.0.5)** - Consider adding:
- Release deployment automation
- A/B testing support
- Release approval workflows

---

## Phase 5 Priorities - TIER 3 Specialized

### Webhooks
**Gap:** 5 endpoints, 0% coverage
**Extension:** `WebhooksExt`
**Use Cases:** Event-driven architectures, external system integration
**Estimated Effort:** 1 week

### Credentials & Security
**Gap:** 7 endpoints, 0% coverage
**Extension:** `CredentialsExt`
**Use Cases:** CyberArk, Azure Key Vault, HashiCorp Vault integration
**Estimated Effort:** 1 week

### Users & Roles (RBAC)
**Gap:** 15 endpoints, 0% coverage
**Extensions:** `UsersExt`, `RolesExt`
**Use Cases:** User provisioning, permission management, SSO
**Estimated Effort:** 2 weeks
**Note:** Security-sensitive, may require official SDK support

### Machines
**Gap:** 5 endpoints, 0% coverage
**Extension:** `MachinesExt`
**Use Cases:** VM provisioning, machine pool management
**Estimated Effort:** 1 week

### Business Rules
**Gap:** 7 endpoints, 0% coverage
**Extension:** `BusinessRulesExt`
**Use Cases:** Dynamic decision logic, rule engines
**Estimated Effort:** 1.5 weeks

### Execution Media
**Gap:** 4 endpoints, 0% coverage
**Extension:** `ExecutionMediaExt`
**Use Cases:** Recordings, screenshots, execution artifacts
**Estimated Effort:** 1 week

---

## Complete API Surface Breakdown

### Orchestrator API Families (100+ families, 339 endpoints)

**TIER 1 - Zero Coverage, High Demand:**
- ❌ TestAutomation (29 endpoints) - **HIGHEST PRIORITY**
- ❌ Stats/Monitoring (16 endpoints)
- ❌ Robots (21 endpoints)

**TIER 2 - Partial Coverage, Core Operations:**
- ✅ Assets (9 endpoints) - **COMPLETE v0.0.5**
- ✅ Jobs (10 endpoints) - **COMPLETE v0.0.5**
- ✅ Queues (16 endpoints) - **COMPLETE v0.0.5**
- ✅ Processes/Releases (18 endpoints) - **COMPLETE v0.0.5**
- ✅ Buckets (12 endpoints) - **COMPLETE v0.0.1**
- ✅ Folders (24 endpoints) - **COMPLETE v0.0.5**

**TIER 3 - Zero Coverage, Specialized:**
- ❌ Schedules (6 endpoints) - **COMPLETE v0.0.5** ✅
- ❌ Libraries (5 endpoints) - **COMPLETE v0.0.5** ✅
- ❌ Tasks/Forms (38 endpoints) - **COMPLETE v0.0.5** ✅
- ❌ Webhooks (5 endpoints)
- ❌ CredentialStores (7 endpoints)
- ❌ Users (10 endpoints)
- ❌ Roles (5 endpoints)
- ❌ Machines (5 endpoints)
- ❌ BusinessRules (7 endpoints)
- ❌ ExecutionMedia (4 endpoints)
- ❌ Calendars (3 endpoints)
- ❌ DirectoryService (4 endpoints)
- ❌ PersonalWorkspaces (5 endpoints)
- ❌ Licensing (4 endpoints) - Rarely needed
- ❌ Settings (17 endpoints) - Admin-focused
- ❌ Maintenance (3 endpoints) - Host admin only
- ❌ Tenants (2 endpoints) - Host admin only
- ❌ Permissions (1 endpoint)
- ❌ Translations (1 endpoint)
- ❌ Alerts (4 endpoints) - DEPRECATED

---

## Technical Architecture

### Design Principles

1. **Composition over Inheritance** - Wrap SDK, don't replace it
2. **Automatic Authentication** - Leverage `sdk.api_client` for auth and retry logic
3. **Minimal Dependencies** - Only require the UiPath SDK
4. **Type-Safe** - Full type hints for IDE autocomplete
5. **Production-Ready** - Comprehensive error handling and logging
6. **Caching Strategy** - Folder ID caching reduces API calls by 33%

### Implementation Pattern

```python
class ExtensionExt:
    """Extension for [API Family] operations."""

    def __init__(self, sdk: UiPath):
        """Initialize with UiPath SDK instance."""
        self.sdk = sdk
        # Optional: Initialize shared utilities
        # self.folder_utils = FolderUtils(sdk)

    def operation(
        self,
        required_param: str,
        folder_key: Optional[str] = None,
        optional_param: Optional[str] = None
    ) -> ReturnType:
        """Operation description.

        Args:
            required_param: Description
            folder_key: Folder GUID (optional)
            optional_param: Description (optional)

        Returns:
            Description of return value

        Raises:
            Exception: Conditions that raise exceptions

        Example:
            >>> ext = ExtensionExt(sdk)
            >>> result = ext.operation("value", folder_key="5ebb73c3-...")
        """
        # Build request parameters
        params = {}
        if optional_param:
            params["param"] = optional_param

        # Build headers (folder context)
        headers = {}
        if folder_key:
            headers["x-uipath-folderkey"] = folder_key

        # Make API request
        response = self.sdk.api_client.request(
            "GET",  # or POST, PATCH, DELETE
            "/odata/Endpoint",
            params=params,
            headers=headers
        )

        return response.json()
```

### Header Management

Different API families require different headers:

| API Family | Header | Value Type |
|------------|--------|------------|
| Context Grounding | `x-uipath-folderkey` | GUID |
| Storage Buckets | `X-UIPATH-OrganizationUnitId` | Numeric ID |
| OData Folders | `x-uipath-folderkey` | GUID |
| Most OData | `x-uipath-folderkey` | GUID |

**FolderUtils** handles conversion and caching automatically.

---

## Packaging Strategy

### Current Approach (Monorepo)

**Pros:**
- Single package installation
- Unified versioning
- Shared utilities (FolderUtils)
- Easier dependency management

**Cons:**
- Larger package size
- All dependencies bundled

**Recommendation:** Continue for core infrastructure (Phases 1-3)

### Future Consideration (Separate Packages)

**When to split:**
- Specialized domains (TIER 3)
- Optional heavy dependencies
- Different release cycles

**Example Structure:**
```
uipath-sdk-extensions       # Core: Storage, Assets, Jobs, Queues, Processes
uipath-test-automation-ext  # Test automation only
uipath-monitoring-ext       # Stats, audit logs
uipath-robots-ext           # Robot management
uipath-tasks-ext            # Forms and tasks
```

---

## Development Guidelines

### Adding a New Extension

1. **Create Extension File** - `src/uipath_sdk_extensions/new_ext.py`
2. **Implement Methods** - Follow pattern above
3. **Add Type Hints** - Full typing for all methods
4. **Write Docstrings** - Include examples in docstrings
5. **Update `__init__.py`** - Export new class
6. **Update Documentation** - README, ALPHA_TESTING, this file
7. **Test Locally** - Verify against live Orchestrator instance
8. **Bump Version** - Update version in pyproject.toml

### Code Quality Standards

- **Type Hints:** 100% coverage
- **Docstrings:** All public methods
- **Examples:** Include in docstrings
- **Error Handling:** Descriptive exceptions
- **Consistent Naming:** follow_python_conventions
- **No Emojis:** In code or commits (per user preferences)

### Testing Strategy

**Manual Testing:**
- Verify against live Orchestrator instance
- Test folder context handling (GUID vs numeric ID)
- Test error scenarios (missing resources, permissions)
- Test caching behavior

**Future:**
- Unit tests with mocked SDK
- Integration tests against test tenant
- CI/CD pipeline for automated testing

---

## Success Metrics

### Coverage Metrics
- **Current:** 25% of 339 endpoints
- **Phase 3 Target:** 40% (adding TestAutomation + Monitoring + Robots)
- **Long-term Goal:** 60% (TIER 1 + TIER 2 complete)

### Developer Impact
- **LOC Reduction:** 150+ LOC → 3-5 lines
- **API Call Reduction:** 33% fewer calls (folder caching)
- **Time Savings:** Hours → minutes for common tasks

### Adoption Metrics
- MyGet package downloads
- GitHub stars/forks
- Community feedback/issues
- UiPath Community forum mentions

---

## Community Feedback Priorities

**Questions for Users:**

1. **Phase 3 Priority** - Which extension do you need most?
   - TestAutomationExt (CI/CD automation)
   - MonitoringExt (dashboards, analytics)
   - RobotsExt (fleet management)

2. **Phase 2 Feedback** - Which v0.0.5 extensions are most valuable?
   - AssetsExt, JobsExt, QueuesExt, ProcessesExt
   - SchedulesExt, LibrariesExt, TasksExt, FolderManagementExt

3. **Missing Functionality** - What operations are you manually implementing?

4. **Integration Patterns** - How are you using the extensions?
   - CI/CD pipelines
   - Monitoring dashboards
   - Administrative automation
   - Testing frameworks

**Feedback Channels:**
- GitHub Gist: [cprima/10c7bbc6](https://gist.github.com/cprima/10c7bbc65dd578940c7654d13d083d9e)
- GitHub Issues (when repository is public)

---

## References

- **Package:** [uipath-sdk-extensions on MyGet](https://www.myget.org/feed/cprima-forge/package/pythonwhl/uipath-sdk-extensions)
- **UiPath Python SDK:** https://github.com/UiPath/uipath-python
- **Orchestrator API Spec:** `{base_url}/swagger/` (Swagger v20.0)
- **RFC Document:** [docs/RfC.md](docs/RfC.md)
- **Alpha Testing Guide:** [ALPHA_TESTING.md](ALPHA_TESTING.md)

---

**Last Updated:** 2025-10-26
**Maintainer:** Christian Prior-Mamulyan
