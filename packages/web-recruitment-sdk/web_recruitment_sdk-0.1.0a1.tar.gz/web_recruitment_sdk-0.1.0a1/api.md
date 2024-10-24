# Shared Types

```python
from web_recruitment_sdk.types import (
    CriteriaRead,
    PatientRead,
    ProtocolParsingRead,
    ProtocolRead,
    SiteRead,
)
```

# Admin

## Accounts

Types:

```python
from web_recruitment_sdk.types.admin import AccountRead, UserWithAccount, AccountListResponse
```

Methods:

- <code title="post /admin/accounts">client.admin.accounts.<a href="./src/web_recruitment_sdk/resources/admin/accounts/accounts.py">create</a>(\*\*<a href="src/web_recruitment_sdk/types/admin/account_create_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/admin/account_read.py">AccountRead</a></code>
- <code title="get /admin/accounts/{account_id}">client.admin.accounts.<a href="./src/web_recruitment_sdk/resources/admin/accounts/accounts.py">retrieve</a>(account_id) -> <a href="./src/web_recruitment_sdk/types/admin/account_read.py">AccountRead</a></code>
- <code title="get /admin/accounts">client.admin.accounts.<a href="./src/web_recruitment_sdk/resources/admin/accounts/accounts.py">list</a>(\*\*<a href="src/web_recruitment_sdk/types/admin/account_list_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/admin/account_list_response.py">AccountListResponse</a></code>

### Me

Methods:

- <code title="get /admin/accounts/me">client.admin.accounts.me.<a href="./src/web_recruitment_sdk/resources/admin/accounts/me.py">retrieve</a>() -> <a href="./src/web_recruitment_sdk/types/admin/user_with_account.py">UserWithAccount</a></code>

## Users

Types:

```python
from web_recruitment_sdk.types.admin import UserRead, UserRoleRead, UserListResponse
```

Methods:

- <code title="post /admin/users">client.admin.users.<a href="./src/web_recruitment_sdk/resources/admin/users.py">create</a>(\*\*<a href="src/web_recruitment_sdk/types/admin/user_create_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/admin/user_read.py">UserRead</a></code>
- <code title="get /admin/users/{email}">client.admin.users.<a href="./src/web_recruitment_sdk/resources/admin/users.py">retrieve</a>(email) -> <a href="./src/web_recruitment_sdk/types/admin/user_read.py">UserRead</a></code>
- <code title="get /admin/users">client.admin.users.<a href="./src/web_recruitment_sdk/resources/admin/users.py">list</a>(\*\*<a href="src/web_recruitment_sdk/types/admin/user_list_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/admin/user_list_response.py">UserListResponse</a></code>
- <code title="delete /admin/users/{email}">client.admin.users.<a href="./src/web_recruitment_sdk/resources/admin/users.py">delete</a>(email) -> None</code>

## Roles

Types:

```python
from web_recruitment_sdk.types.admin import RoleRead, RoleListResponse
```

Methods:

- <code title="get /admin/roles/{role_id}">client.admin.roles.<a href="./src/web_recruitment_sdk/resources/admin/roles.py">retrieve</a>(role_id) -> <a href="./src/web_recruitment_sdk/types/admin/role_read.py">RoleRead</a></code>
- <code title="get /admin/roles">client.admin.roles.<a href="./src/web_recruitment_sdk/resources/admin/roles.py">list</a>(\*\*<a href="src/web_recruitment_sdk/types/admin/role_list_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/admin/role_list_response.py">RoleListResponse</a></code>

# Health

Types:

```python
from web_recruitment_sdk.types import HealthRetrieveResponse
```

Methods:

- <code title="get /health">client.health.<a href="./src/web_recruitment_sdk/resources/health.py">retrieve</a>() -> <a href="./src/web_recruitment_sdk/types/health_retrieve_response.py">object</a></code>

# Patients

Types:

```python
from web_recruitment_sdk.types import PatientListResponse
```

Methods:

- <code title="post /patients">client.patients.<a href="./src/web_recruitment_sdk/resources/patients/patients.py">create</a>(\*\*<a href="src/web_recruitment_sdk/types/patient_create_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/shared/patient_read.py">PatientRead</a></code>
- <code title="get /patients/{patient_id}">client.patients.<a href="./src/web_recruitment_sdk/resources/patients/patients.py">retrieve</a>(patient_id) -> <a href="./src/web_recruitment_sdk/types/shared/patient_read.py">PatientRead</a></code>
- <code title="get /patients">client.patients.<a href="./src/web_recruitment_sdk/resources/patients/patients.py">list</a>(\*\*<a href="src/web_recruitment_sdk/types/patient_list_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/patient_list_response.py">PatientListResponse</a></code>

## Protocol

Types:

```python
from web_recruitment_sdk.types.patients import ProtocolRetrieveResponse
```

Methods:

- <code title="get /patients/protocol/{protocol_id}">client.patients.protocol.<a href="./src/web_recruitment_sdk/resources/patients/protocol.py">retrieve</a>(protocol_id, \*\*<a href="src/web_recruitment_sdk/types/patients/protocol_retrieve_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/patients/protocol_retrieve_response.py">ProtocolRetrieveResponse</a></code>

# PatientsByExternalID

Methods:

- <code title="get /patients_by_external_id/{external_id}">client.patients_by_external_id.<a href="./src/web_recruitment_sdk/resources/patients_by_external_id.py">retrieve</a>(external_id) -> <a href="./src/web_recruitment_sdk/types/shared/patient_read.py">PatientRead</a></code>

# Protocols

Types:

```python
from web_recruitment_sdk.types import ProtocolListResponse
```

Methods:

- <code title="post /protocols">client.protocols.<a href="./src/web_recruitment_sdk/resources/protocols/protocols.py">create</a>(\*\*<a href="src/web_recruitment_sdk/types/protocol_create_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/shared/protocol_read.py">ProtocolRead</a></code>
- <code title="get /protocols/{protocol_id}">client.protocols.<a href="./src/web_recruitment_sdk/resources/protocols/protocols.py">retrieve</a>(protocol_id) -> <a href="./src/web_recruitment_sdk/types/shared/protocol_read.py">ProtocolRead</a></code>
- <code title="patch /protocols/{protocol_id}">client.protocols.<a href="./src/web_recruitment_sdk/resources/protocols/protocols.py">update</a>(protocol_id, \*\*<a href="src/web_recruitment_sdk/types/protocol_update_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/shared/protocol_read.py">ProtocolRead</a></code>
- <code title="get /protocols">client.protocols.<a href="./src/web_recruitment_sdk/resources/protocols/protocols.py">list</a>() -> <a href="./src/web_recruitment_sdk/types/protocol_list_response.py">ProtocolListResponse</a></code>
- <code title="delete /protocols/{protocol_id}">client.protocols.<a href="./src/web_recruitment_sdk/resources/protocols/protocols.py">delete</a>(protocol_id) -> None</code>

## Matches

Types:

```python
from web_recruitment_sdk.types.protocols import PatientMatch, MatchListResponse
```

Methods:

- <code title="get /protocols/{protocol_id}/matches">client.protocols.matches.<a href="./src/web_recruitment_sdk/resources/protocols/matches.py">list</a>(protocol_id) -> <a href="./src/web_recruitment_sdk/types/protocols/match_list_response.py">MatchListResponse</a></code>

## Criteria

Types:

```python
from web_recruitment_sdk.types.protocols import CriterionListResponse
```

Methods:

- <code title="get /protocols/{protocol_id}/criteria">client.protocols.criteria.<a href="./src/web_recruitment_sdk/resources/protocols/criteria.py">list</a>(protocol_id) -> <a href="./src/web_recruitment_sdk/types/protocols/criterion_list_response.py">CriterionListResponse</a></code>

## CriteriaInstances

Types:

```python
from web_recruitment_sdk.types.protocols import (
    CriteriaInstanceWithCriteriaType,
    CriteriaInstanceListResponse,
)
```

Methods:

- <code title="get /protocols/{protocol_id}/criteria_instances">client.protocols.criteria_instances.<a href="./src/web_recruitment_sdk/resources/protocols/criteria_instances.py">list</a>(protocol_id, \*\*<a href="src/web_recruitment_sdk/types/protocols/criteria_instance_list_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/protocols/criteria_instance_list_response.py">CriteriaInstanceListResponse</a></code>

## ProtocolParsing

Methods:

- <code title="get /protocols/{protocol_id}/protocol-parsing">client.protocols.protocol_parsing.<a href="./src/web_recruitment_sdk/resources/protocols/protocol_parsing.py">retrieve</a>(protocol_id) -> <a href="./src/web_recruitment_sdk/types/shared/protocol_parsing_read.py">ProtocolParsingRead</a></code>

## Sites

Types:

```python
from web_recruitment_sdk.types.protocols import ProtocolSites, SiteListResponse
```

Methods:

- <code title="post /protocols/{protocol_id}/sites/{site_id}">client.protocols.sites.<a href="./src/web_recruitment_sdk/resources/protocols/sites.py">create</a>(site_id, \*, protocol_id) -> <a href="./src/web_recruitment_sdk/types/protocols/protocol_sites.py">ProtocolSites</a></code>
- <code title="get /protocols/{protocol_id}/sites">client.protocols.sites.<a href="./src/web_recruitment_sdk/resources/protocols/sites.py">list</a>(protocol_id) -> <a href="./src/web_recruitment_sdk/types/protocols/site_list_response.py">SiteListResponse</a></code>
- <code title="delete /protocols/{protocol_id}/sites/{site_id}">client.protocols.sites.<a href="./src/web_recruitment_sdk/resources/protocols/sites.py">delete</a>(site_id, \*, protocol_id) -> None</code>

# Criteria

Methods:

- <code title="post /criteria">client.criteria.<a href="./src/web_recruitment_sdk/resources/criteria.py">create</a>(\*\*<a href="src/web_recruitment_sdk/types/criterion_create_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/shared/criteria_read.py">CriteriaRead</a></code>
- <code title="get /criteria/{criteria_id}">client.criteria.<a href="./src/web_recruitment_sdk/resources/criteria.py">retrieve</a>(criteria_id) -> <a href="./src/web_recruitment_sdk/types/shared/criteria_read.py">CriteriaRead</a></code>
- <code title="put /criteria/{criterion_id}">client.criteria.<a href="./src/web_recruitment_sdk/resources/criteria.py">update</a>(criterion_id, \*\*<a href="src/web_recruitment_sdk/types/criterion_update_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/shared/criteria_read.py">CriteriaRead</a></code>

# CriteriaInstances

Types:

```python
from web_recruitment_sdk.types import CriteriaInstanceRead, CriteriaInstanceCreateResponse
```

Methods:

- <code title="post /criteria_instances">client.criteria_instances.<a href="./src/web_recruitment_sdk/resources/criteria_instances.py">create</a>(\*\*<a href="src/web_recruitment_sdk/types/criteria_instance_create_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/criteria_instance_create_response.py">CriteriaInstanceCreateResponse</a></code>

# Appointments

Types:

```python
from web_recruitment_sdk.types import (
    AppointmentRead,
    AppointmentListResponse,
    AppointmentBulkResponse,
)
```

Methods:

- <code title="post /appointments">client.appointments.<a href="./src/web_recruitment_sdk/resources/appointments.py">create</a>(\*\*<a href="src/web_recruitment_sdk/types/appointment_create_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/appointment_read.py">AppointmentRead</a></code>
- <code title="get /appointments/{appointment_id}">client.appointments.<a href="./src/web_recruitment_sdk/resources/appointments.py">retrieve</a>(appointment_id) -> <a href="./src/web_recruitment_sdk/types/appointment_read.py">AppointmentRead</a></code>
- <code title="put /appointments/{appointment_id}">client.appointments.<a href="./src/web_recruitment_sdk/resources/appointments.py">update</a>(appointment_id, \*\*<a href="src/web_recruitment_sdk/types/appointment_update_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/appointment_read.py">AppointmentRead</a></code>
- <code title="get /appointments">client.appointments.<a href="./src/web_recruitment_sdk/resources/appointments.py">list</a>(\*\*<a href="src/web_recruitment_sdk/types/appointment_list_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/appointment_list_response.py">AppointmentListResponse</a></code>
- <code title="delete /appointments/{appointment_id}">client.appointments.<a href="./src/web_recruitment_sdk/resources/appointments.py">delete</a>(appointment_id) -> None</code>
- <code title="post /appointments/bulk">client.appointments.<a href="./src/web_recruitment_sdk/resources/appointments.py">bulk</a>(\*\*<a href="src/web_recruitment_sdk/types/appointment_bulk_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/appointment_bulk_response.py">AppointmentBulkResponse</a></code>

# Sites

Types:

```python
from web_recruitment_sdk.types import SiteListResponse
```

Methods:

- <code title="post /sites">client.sites.<a href="./src/web_recruitment_sdk/resources/sites.py">create</a>(\*\*<a href="src/web_recruitment_sdk/types/site_create_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/shared/site_read.py">SiteRead</a></code>
- <code title="get /sites/{site_id}">client.sites.<a href="./src/web_recruitment_sdk/resources/sites.py">retrieve</a>(site_id) -> <a href="./src/web_recruitment_sdk/types/shared/site_read.py">SiteRead</a></code>
- <code title="get /sites">client.sites.<a href="./src/web_recruitment_sdk/resources/sites.py">list</a>() -> <a href="./src/web_recruitment_sdk/types/site_list_response.py">SiteListResponse</a></code>

# ProtocolParsing

Types:

```python
from web_recruitment_sdk.types import (
    ProtocolParsingListResponse,
    ProtocolParsingErrorResponse,
    ProtocolParsingSuccessResponse,
)
```

Methods:

- <code title="post /protocol-parsing">client.protocol_parsing.<a href="./src/web_recruitment_sdk/resources/protocol_parsing.py">create</a>(\*\*<a href="src/web_recruitment_sdk/types/protocol_parsing_create_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/shared/protocol_read.py">ProtocolRead</a></code>
- <code title="get /protocol-parsing">client.protocol_parsing.<a href="./src/web_recruitment_sdk/resources/protocol_parsing.py">list</a>(\*\*<a href="src/web_recruitment_sdk/types/protocol_parsing_list_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/protocol_parsing_list_response.py">ProtocolParsingListResponse</a></code>
- <code title="post /protocol-parsing/{job_id}/{tenant}/error">client.protocol_parsing.<a href="./src/web_recruitment_sdk/resources/protocol_parsing.py">error</a>(tenant, \*, job_id, \*\*<a href="src/web_recruitment_sdk/types/protocol_parsing_error_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/protocol_parsing_error_response.py">object</a></code>
- <code title="post /protocol-parsing/{job_id}/{tenant}/success">client.protocol_parsing.<a href="./src/web_recruitment_sdk/resources/protocol_parsing.py">success</a>(tenant, \*, job_id, \*\*<a href="src/web_recruitment_sdk/types/protocol_parsing_success_params.py">params</a>) -> <a href="./src/web_recruitment_sdk/types/protocol_parsing_success_response.py">object</a></code>
