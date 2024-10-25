# CHANGELOG


## v1.10.2 (2024-10-25)

### Bug Fixes

* fix: ensure filepath is set to the required value before waiting ([`db9e191`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/db9e191e4a5c1ee340094400dff93b7ba10f8dfb))


## v1.10.1 (2024-10-25)

### Bug Fixes

* fix: ophyd patch, compatibility with Python >=3.12

"find_module" has been deleted from Finder class ([`97982dd`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/97982dd1385f065b04aa780c91aee9f67b9beda2))

### Refactoring

* refactor: Refactored SimCamera write_to_disk option to continously write to h5 file. ([`41c54aa`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/41c54aa851e7fcf22b139aeb041d000395524b7e))


## v1.10.0 (2024-10-22)

### Bug Fixes

* fix: improved patching of Ophyd 1.9 ([`8a9a6a9`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/8a9a6a9910b44d55412e80443f145d629b1cfc2f))

### Features

* feat: add test device for return status for stage/unstage ([`f5ab78e`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/f5ab78e933c2bbb34c571a72c25a7fc5c2b20e65))

### Unknown

* tests: add 'conftest.py' with ophyd_devices import to ensure ophyd is always patched, first ([`3a1202d`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/3a1202d0d894120f786af80a8873d0fd049e417a))


## v1.9.6 (2024-10-17)

### Bug Fixes

* fix: cleanup and bugfix in positioner; closes #84 ([`6a7c074`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/6a7c0745e33a2b2cc561b42ad90e61ac08fb9d51))

### Refactoring

* refactor: cleanup sim module namespace; closes #80 ([`fa32b42`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/fa32b4234b786d93ddf872c7a8220f2d0518b465))


## v1.9.5 (2024-10-01)

### Bug Fixes

* fix: bugfix for proxy devices ([`b1639ea`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/b1639ea3baddec722a444b7c65bdc39d763b7d07))

* fix: Fixed SimWaveform, works as async device and device_monitor_1d simultaneously ([`7ff37c0`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/7ff37c0dcdd87bfa8f518b1dd7acc4aab353b71f))

### Refactoring

* refactor: cleanup of scan_status prints in scaninfo_mixin ([`449dadb`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/449dadb593a0432d31f905e4e507102d0c4f3fd6))


## v1.9.4 (2024-10-01)

### Bug Fixes

* fix: increased min version of typeguard ([`e379282`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/e3792826644e01adf84435891d500ec5bef85cda))

### Build System

* build: allow numpy v2 ([`825a7de`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/825a7dee5e948d9decb4e8649c0573a2d9d4b83f))


## v1.9.3 (2024-09-06)

### Bug Fixes

* fix: remove bodge (readback) in SimMonitor ([`cd75fc0`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/cd75fc0e01e565445f7176e52faada264544d439))


## v1.9.2 (2024-09-05)

### Bug Fixes

* fix: change inheritance for simmonitor from device to signal ([`a675420`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/a6754208a0991f8ccf546cbb2bee015f6daecb93))

* fix: fix inheritance for SimMonitor ([`f56961b`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/f56961ba8c179d4ca75e574fd8565ae4c3f41eed))

### Continuous Integration

* ci: prefill variables for manual pipeline start ([`3f2c6dc`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/3f2c6dc4efddfa06bebff13ac2984e45efd13a90))

### Refactoring

* refactor: bodge to make simmonitor compatible with tests; to be removed asap ([`9d9a5fe`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/9d9a5fe305981f845c87e3417dd1072d2b8692b0))


## v1.9.1 (2024-08-28)

### Bug Fixes

* fix: removed arguments for callback call ([`d83c102`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/d83c102d14430b9acd8525d1d61e6e092d9f6043))

### Refactoring

* refactor: moved sim test devices to sim_test_devices ([`a49c6f6`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/a49c6f6a625a576524fceca62dd0a1582a4a4a7d))


## v1.9.0 (2024-08-28)

### Features

* feat: add dual patch pvs to ophyd_devices ([`c47918d`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/c47918d6e7ff41721aa4fa67043ff6cd1aeee2c7))


## v1.8.1 (2024-08-15)

### Bug Fixes

* fix: fixed import of simpositioner test devices ([`f1f9721`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/f1f9721fe9c71da747558e4bb005c04592aa2bde))

### Build System

* build: moved pyepics deps to >=3.5.5

3.5.3 and 3.5.4 should not be used ([`8046f22`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/8046f22a807f94f1dc7d9ab77ab3b9c3ce821633))


## v1.8.0 (2024-08-14)

### Features

* feat(sim): added dedicated positioner with controller ([`4ad5723`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/4ad57230e327c3714a03ae138bc12a5028acb1dd))


## v1.7.3 (2024-08-08)

### Bug Fixes

* fix: small bugfix to ensure motor_is_moving updates at the end of a move ([`577b35f`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/577b35f287ec997a41ce27fae2db9bbc669a2d9d))

### Testing

* test: add test case ([`76e1cfc`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/76e1cfc4aade9c691d9b5bfd4db0b678b7e2f1cc))


## v1.7.2 (2024-07-29)

### Bug Fixes

* fix: add write_access attribute to simulated readonly signal ([`c3e17ba`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/c3e17ba05632309adcc896f858e52ecb07048a30))

* fix: remove print for select_model method of sim module ([`5009316`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/5009316a82897d739b2a26eb341e9f5a1e083e51))

* fix: Improve asyn_monitor and camera on_trigger and on_complete to return status ([`f311876`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/f3118765b0efc38dd12a3d72d290e517490f9fbf))

### Continuous Integration

* ci: made BEC a child pipeline ([`9eb67a0`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/9eb67a0900159248e785b17e4250ae6a7e954348))

* ci: moved to awi utils trigger pipelines ([`0f6494a`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/0f6494ae2caafc0727a394683718031670614aeb))

* ci: changed default branch ([`fe5f1c3`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/fe5f1c314f51cb07bae4044a406ed5dc738c7837))

### Refactoring

* refactor: review DeviceStatus and error handling in simulation ([`87858ed`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/87858edfe290cb711bc30c2f3ba2653460d15af6))

### Testing

* test: Fix and add test scenarios for DeviceStatus error handling ([`4397db9`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/4397db919a852d70c53d80a532540eaabdffc3ad))

* test: adapt tests to consider returned DeviceStatus for on_trigger/complete ([`f8e9aaf`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/f8e9aaf55a5734f3bf557bbf5e51eb7ea41257d4))

### Unknown

* wip ([`35141e9`](https://gitlab.psi.ch/bec/ophyd_devices/-/commit/35141e94b1c8a6ba70e96b915b45871d19bd5f7e))
