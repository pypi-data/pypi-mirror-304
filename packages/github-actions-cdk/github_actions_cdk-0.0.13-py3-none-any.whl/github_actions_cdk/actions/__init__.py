from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

from .. import (
    Action as _Action_64902b3f,
    ActionProps as _ActionProps_ebcddbbb,
    Job as _Job_0ed15d61,
    Step as _Step_edd90555,
)


class Checkout(
    _Action_64902b3f,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.actions.Checkout",
):
    '''(experimental) The Checkout action, which checks out a Git repository at a specified version in a GitHub Actions workflow.

    The Checkout class provides settings for cloning a repository, allowing
    additional parameters for authentication, configuration, and clone options.

    :stability: experimental
    '''

    def __init__(
        self,
        id: builtins.str,
        *,
        clean: typing.Optional[builtins.bool] = None,
        fetch_depth: typing.Optional[jsii.Number] = None,
        fetch_tags: typing.Optional[builtins.bool] = None,
        filter: typing.Optional[builtins.str] = None,
        github_server_url: typing.Optional[builtins.str] = None,
        lfs: typing.Optional[builtins.bool] = None,
        path: typing.Optional[builtins.str] = None,
        persist_credentials: typing.Optional[builtins.bool] = None,
        ref: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        set_safe_directory: typing.Optional[builtins.bool] = None,
        show_progress: typing.Optional[builtins.bool] = None,
        sparse_checkout: typing.Optional[typing.Sequence[builtins.str]] = None,
        sparse_checkout_cone_mode: typing.Optional[builtins.bool] = None,
        ssh_key: typing.Optional[builtins.str] = None,
        ssh_known_hosts: typing.Optional[builtins.str] = None,
        ssh_strict: typing.Optional[builtins.bool] = None,
        ssh_user: typing.Optional[builtins.str] = None,
        submodules: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
        token: typing.Optional[builtins.str] = None,
        version: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Constructs a Checkout action with the specified ID and properties.

        :param id: - The unique identifier for the action within a workflow.
        :param clean: (experimental) Whether to run ``git clean -ffdx && git reset --hard HEAD`` before fetching. Default: true
        :param fetch_depth: (experimental) Number of commits to fetch. ``0`` indicates all history for all branches and tags. Default: 1
        :param fetch_tags: (experimental) Whether to fetch tags even if ``fetchDepth > 0``. Default: false
        :param filter: (experimental) Filter for partially cloning the repository. Overrides ``sparseCheckout`` if set.
        :param github_server_url: (experimental) Base URL for the GitHub instance to clone from. Uses environment defaults if not specified.
        :param lfs: (experimental) Whether to download Git LFS (Large File Storage) files. Default: false
        :param path: (experimental) Path under ``$GITHUB_WORKSPACE`` to place the repository.
        :param persist_credentials: (experimental) Configures the token or SSH key in the local git configuration. Default: true
        :param ref: (experimental) The branch, tag, or SHA to checkout. Defaults to the reference or SHA for the triggering event, or the default branch otherwise.
        :param repository: (experimental) Repository name with owner, for example, ``actions/checkout``. Default: github.repository
        :param set_safe_directory: (experimental) Adds the repository path to ``safe.directory`` in the Git global configuration. Default: true
        :param show_progress: (experimental) Whether to show progress status output while fetching. Default: true
        :param sparse_checkout: (experimental) Patterns for sparse checkout. Only the specified directories or files will be checked out.
        :param sparse_checkout_cone_mode: (experimental) Whether to use cone mode when performing a sparse checkout. Default: true
        :param ssh_key: (experimental) SSH key used to fetch the repository, enabling authenticated git commands.
        :param ssh_known_hosts: (experimental) Known hosts to add to the SSH configuration. Public SSH keys for a host can be obtained with ``ssh-keyscan``, e.g., ``ssh-keyscan github.com``.
        :param ssh_strict: (experimental) Whether to perform strict host key checking. When ``true``, adds strict SSH configuration options to the command line. Default: true
        :param ssh_user: (experimental) User for connecting to the SSH host. Defaults to 'git'. Default: "git"
        :param submodules: (experimental) Whether to checkout submodules, with options for ``true`` (checkout submodules) or ``recursive`` (checkout submodules recursively). Default: false
        :param token: (experimental) Personal Access Token (PAT) used to fetch the repository, enabling authenticated git commands. Default: github.token
        :param version: (experimental) The version of the action, can be a specific version, tag, or commit SHA.
        :param name: (experimental) Optional name for the action, displayed in logs.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1830fde06e0939430f30c3b1ec33ce537d1db25383e2ed028b1573eec5580451)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CheckoutProps(
            clean=clean,
            fetch_depth=fetch_depth,
            fetch_tags=fetch_tags,
            filter=filter,
            github_server_url=github_server_url,
            lfs=lfs,
            path=path,
            persist_credentials=persist_credentials,
            ref=ref,
            repository=repository,
            set_safe_directory=set_safe_directory,
            show_progress=show_progress,
            sparse_checkout=sparse_checkout,
            sparse_checkout_cone_mode=sparse_checkout_cone_mode,
            ssh_key=ssh_key,
            ssh_known_hosts=ssh_known_hosts,
            ssh_strict=ssh_strict,
            ssh_user=ssh_user,
            submodules=submodules,
            token=token,
            version=version,
            name=name,
        )

        jsii.create(self.__class__, self, [id, props])

    @jsii.member(jsii_name="bind")
    def bind(self, job: _Job_0ed15d61) -> _Step_edd90555:
        '''(experimental) Binds the checkout action to a job, adding a step to the workflow that checks out the repository based on the defined properties.

        :param job: - The job to bind the checkout step to.

        :return: A ``Step`` representing the configured checkout action within the job.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7f0a73ca3133b853cf44ee1014c16c956601bc137b20a8eba70009e9702ec37)
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
        return typing.cast(_Step_edd90555, jsii.invoke(self, "bind", [job]))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> "CheckoutOutputs":
        '''(experimental) Retrieves the outputs of the Checkout action as specified in the GitHub Actions context.

        This method returns an object containing output values that can be referenced in subsequent
        steps of the workflow, such as the checked-out reference and commit.

        :return: An object containing the output values of the action.

        :stability: experimental
        '''
        return typing.cast("CheckoutOutputs", jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="clean")
    def clean(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "clean"))

    @builtins.property
    @jsii.member(jsii_name="fetchDepth")
    def fetch_depth(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fetchDepth"))

    @builtins.property
    @jsii.member(jsii_name="fetchTags")
    def fetch_tags(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "fetchTags"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "filter"))

    @builtins.property
    @jsii.member(jsii_name="githubServerUrl")
    def github_server_url(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "githubServerUrl"))

    @builtins.property
    @jsii.member(jsii_name="lfs")
    def lfs(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "lfs"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @builtins.property
    @jsii.member(jsii_name="persistCredentials")
    def persist_credentials(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "persistCredentials"))

    @builtins.property
    @jsii.member(jsii_name="ref")
    def ref(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ref"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repository"))

    @builtins.property
    @jsii.member(jsii_name="setSafeDirectory")
    def set_safe_directory(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "setSafeDirectory"))

    @builtins.property
    @jsii.member(jsii_name="showProgress")
    def show_progress(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "showProgress"))

    @builtins.property
    @jsii.member(jsii_name="sparseCheckout")
    def sparse_checkout(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "sparseCheckout"))

    @builtins.property
    @jsii.member(jsii_name="sparseCheckoutConeMode")
    def sparse_checkout_cone_mode(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "sparseCheckoutConeMode"))

    @builtins.property
    @jsii.member(jsii_name="sshKey")
    def ssh_key(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshKey"))

    @builtins.property
    @jsii.member(jsii_name="sshKnownHosts")
    def ssh_known_hosts(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshKnownHosts"))

    @builtins.property
    @jsii.member(jsii_name="sshStrict")
    def ssh_strict(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "sshStrict"))

    @builtins.property
    @jsii.member(jsii_name="sshUser")
    def ssh_user(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sshUser"))

    @builtins.property
    @jsii.member(jsii_name="submodules")
    def submodules(self) -> typing.Optional[typing.Union[builtins.bool, builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, builtins.str]], jsii.get(self, "submodules"))

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.CheckoutOutputs",
    jsii_struct_bases=[],
    name_mapping={"commit": "commit", "ref": "ref"},
)
class CheckoutOutputs:
    def __init__(self, *, commit: builtins.str, ref: builtins.str) -> None:
        '''(experimental) Output structure for the Checkout action.

        Extends from ActionOutputs to include specific outputs related to
        the checkout process, such as the reference and commit hash.

        :param commit: (experimental) The commit hash of the checked-out version.
        :param ref: (experimental) The reference (branch, tag, or SHA) that was checked out.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__338965b7fbb099ee70e062ffce8e483fd1fa0e4c884043df4b017a6beed355f1)
            check_type(argname="argument commit", value=commit, expected_type=type_hints["commit"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "commit": commit,
            "ref": ref,
        }

    @builtins.property
    def commit(self) -> builtins.str:
        '''(experimental) The commit hash of the checked-out version.

        :stability: experimental
        '''
        result = self._values.get("commit")
        assert result is not None, "Required property 'commit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ref(self) -> builtins.str:
        '''(experimental) The reference (branch, tag, or SHA) that was checked out.

        :stability: experimental
        '''
        result = self._values.get("ref")
        assert result is not None, "Required property 'ref' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckoutOutputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.CheckoutProps",
    jsii_struct_bases=[_ActionProps_ebcddbbb],
    name_mapping={
        "version": "version",
        "name": "name",
        "clean": "clean",
        "fetch_depth": "fetchDepth",
        "fetch_tags": "fetchTags",
        "filter": "filter",
        "github_server_url": "githubServerUrl",
        "lfs": "lfs",
        "path": "path",
        "persist_credentials": "persistCredentials",
        "ref": "ref",
        "repository": "repository",
        "set_safe_directory": "setSafeDirectory",
        "show_progress": "showProgress",
        "sparse_checkout": "sparseCheckout",
        "sparse_checkout_cone_mode": "sparseCheckoutConeMode",
        "ssh_key": "sshKey",
        "ssh_known_hosts": "sshKnownHosts",
        "ssh_strict": "sshStrict",
        "ssh_user": "sshUser",
        "submodules": "submodules",
        "token": "token",
    },
)
class CheckoutProps(_ActionProps_ebcddbbb):
    def __init__(
        self,
        *,
        version: builtins.str,
        name: typing.Optional[builtins.str] = None,
        clean: typing.Optional[builtins.bool] = None,
        fetch_depth: typing.Optional[jsii.Number] = None,
        fetch_tags: typing.Optional[builtins.bool] = None,
        filter: typing.Optional[builtins.str] = None,
        github_server_url: typing.Optional[builtins.str] = None,
        lfs: typing.Optional[builtins.bool] = None,
        path: typing.Optional[builtins.str] = None,
        persist_credentials: typing.Optional[builtins.bool] = None,
        ref: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        set_safe_directory: typing.Optional[builtins.bool] = None,
        show_progress: typing.Optional[builtins.bool] = None,
        sparse_checkout: typing.Optional[typing.Sequence[builtins.str]] = None,
        sparse_checkout_cone_mode: typing.Optional[builtins.bool] = None,
        ssh_key: typing.Optional[builtins.str] = None,
        ssh_known_hosts: typing.Optional[builtins.str] = None,
        ssh_strict: typing.Optional[builtins.bool] = None,
        ssh_user: typing.Optional[builtins.str] = None,
        submodules: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for configuring the Checkout component in a GitHub Actions workflow.

        This interface defines various options available for the Checkout action,
        including authentication, repository reference, and checkout behavior.

        :param version: (experimental) The version of the action, can be a specific version, tag, or commit SHA.
        :param name: (experimental) Optional name for the action, displayed in logs.
        :param clean: (experimental) Whether to run ``git clean -ffdx && git reset --hard HEAD`` before fetching. Default: true
        :param fetch_depth: (experimental) Number of commits to fetch. ``0`` indicates all history for all branches and tags. Default: 1
        :param fetch_tags: (experimental) Whether to fetch tags even if ``fetchDepth > 0``. Default: false
        :param filter: (experimental) Filter for partially cloning the repository. Overrides ``sparseCheckout`` if set.
        :param github_server_url: (experimental) Base URL for the GitHub instance to clone from. Uses environment defaults if not specified.
        :param lfs: (experimental) Whether to download Git LFS (Large File Storage) files. Default: false
        :param path: (experimental) Path under ``$GITHUB_WORKSPACE`` to place the repository.
        :param persist_credentials: (experimental) Configures the token or SSH key in the local git configuration. Default: true
        :param ref: (experimental) The branch, tag, or SHA to checkout. Defaults to the reference or SHA for the triggering event, or the default branch otherwise.
        :param repository: (experimental) Repository name with owner, for example, ``actions/checkout``. Default: github.repository
        :param set_safe_directory: (experimental) Adds the repository path to ``safe.directory`` in the Git global configuration. Default: true
        :param show_progress: (experimental) Whether to show progress status output while fetching. Default: true
        :param sparse_checkout: (experimental) Patterns for sparse checkout. Only the specified directories or files will be checked out.
        :param sparse_checkout_cone_mode: (experimental) Whether to use cone mode when performing a sparse checkout. Default: true
        :param ssh_key: (experimental) SSH key used to fetch the repository, enabling authenticated git commands.
        :param ssh_known_hosts: (experimental) Known hosts to add to the SSH configuration. Public SSH keys for a host can be obtained with ``ssh-keyscan``, e.g., ``ssh-keyscan github.com``.
        :param ssh_strict: (experimental) Whether to perform strict host key checking. When ``true``, adds strict SSH configuration options to the command line. Default: true
        :param ssh_user: (experimental) User for connecting to the SSH host. Defaults to 'git'. Default: "git"
        :param submodules: (experimental) Whether to checkout submodules, with options for ``true`` (checkout submodules) or ``recursive`` (checkout submodules recursively). Default: false
        :param token: (experimental) Personal Access Token (PAT) used to fetch the repository, enabling authenticated git commands. Default: github.token

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbc9a9372aa10e00b2ff916f92a8052e93e51aa4a2ea16b98140884c5a72b662)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument clean", value=clean, expected_type=type_hints["clean"])
            check_type(argname="argument fetch_depth", value=fetch_depth, expected_type=type_hints["fetch_depth"])
            check_type(argname="argument fetch_tags", value=fetch_tags, expected_type=type_hints["fetch_tags"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument github_server_url", value=github_server_url, expected_type=type_hints["github_server_url"])
            check_type(argname="argument lfs", value=lfs, expected_type=type_hints["lfs"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument persist_credentials", value=persist_credentials, expected_type=type_hints["persist_credentials"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument set_safe_directory", value=set_safe_directory, expected_type=type_hints["set_safe_directory"])
            check_type(argname="argument show_progress", value=show_progress, expected_type=type_hints["show_progress"])
            check_type(argname="argument sparse_checkout", value=sparse_checkout, expected_type=type_hints["sparse_checkout"])
            check_type(argname="argument sparse_checkout_cone_mode", value=sparse_checkout_cone_mode, expected_type=type_hints["sparse_checkout_cone_mode"])
            check_type(argname="argument ssh_key", value=ssh_key, expected_type=type_hints["ssh_key"])
            check_type(argname="argument ssh_known_hosts", value=ssh_known_hosts, expected_type=type_hints["ssh_known_hosts"])
            check_type(argname="argument ssh_strict", value=ssh_strict, expected_type=type_hints["ssh_strict"])
            check_type(argname="argument ssh_user", value=ssh_user, expected_type=type_hints["ssh_user"])
            check_type(argname="argument submodules", value=submodules, expected_type=type_hints["submodules"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "version": version,
        }
        if name is not None:
            self._values["name"] = name
        if clean is not None:
            self._values["clean"] = clean
        if fetch_depth is not None:
            self._values["fetch_depth"] = fetch_depth
        if fetch_tags is not None:
            self._values["fetch_tags"] = fetch_tags
        if filter is not None:
            self._values["filter"] = filter
        if github_server_url is not None:
            self._values["github_server_url"] = github_server_url
        if lfs is not None:
            self._values["lfs"] = lfs
        if path is not None:
            self._values["path"] = path
        if persist_credentials is not None:
            self._values["persist_credentials"] = persist_credentials
        if ref is not None:
            self._values["ref"] = ref
        if repository is not None:
            self._values["repository"] = repository
        if set_safe_directory is not None:
            self._values["set_safe_directory"] = set_safe_directory
        if show_progress is not None:
            self._values["show_progress"] = show_progress
        if sparse_checkout is not None:
            self._values["sparse_checkout"] = sparse_checkout
        if sparse_checkout_cone_mode is not None:
            self._values["sparse_checkout_cone_mode"] = sparse_checkout_cone_mode
        if ssh_key is not None:
            self._values["ssh_key"] = ssh_key
        if ssh_known_hosts is not None:
            self._values["ssh_known_hosts"] = ssh_known_hosts
        if ssh_strict is not None:
            self._values["ssh_strict"] = ssh_strict
        if ssh_user is not None:
            self._values["ssh_user"] = ssh_user
        if submodules is not None:
            self._values["submodules"] = submodules
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def version(self) -> builtins.str:
        '''(experimental) The version of the action, can be a specific version, tag, or commit SHA.

        :stability: experimental

        Example::

            version: "v2"
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional name for the action, displayed in logs.

        :stability: experimental

        Example::

            "Checkout Repository"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def clean(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to run ``git clean -ffdx && git reset --hard HEAD`` before fetching.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("clean")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def fetch_depth(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Number of commits to fetch.

        ``0`` indicates all history for all branches and tags.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("fetch_depth")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fetch_tags(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to fetch tags even if ``fetchDepth > 0``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("fetch_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def filter(self) -> typing.Optional[builtins.str]:
        '''(experimental) Filter for partially cloning the repository.

        Overrides ``sparseCheckout`` if set.

        :stability: experimental
        '''
        result = self._values.get("filter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_server_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Base URL for the GitHub instance to clone from.

        Uses environment defaults if not specified.

        :stability: experimental
        '''
        result = self._values.get("github_server_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lfs(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to download Git LFS (Large File Storage) files.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("lfs")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path under ``$GITHUB_WORKSPACE`` to place the repository.

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def persist_credentials(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Configures the token or SSH key in the local git configuration.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("persist_credentials")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ref(self) -> typing.Optional[builtins.str]:
        '''(experimental) The branch, tag, or SHA to checkout.

        Defaults to the reference or SHA for the triggering event,
        or the default branch otherwise.

        :stability: experimental
        '''
        result = self._values.get("ref")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''(experimental) Repository name with owner, for example, ``actions/checkout``.

        :default: github.repository

        :stability: experimental
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def set_safe_directory(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Adds the repository path to ``safe.directory`` in the Git global configuration.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("set_safe_directory")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def show_progress(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to show progress status output while fetching.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("show_progress")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sparse_checkout(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Patterns for sparse checkout.

        Only the specified directories or files will be checked out.

        :stability: experimental
        '''
        result = self._values.get("sparse_checkout")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sparse_checkout_cone_mode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to use cone mode when performing a sparse checkout.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("sparse_checkout_cone_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ssh_key(self) -> typing.Optional[builtins.str]:
        '''(experimental) SSH key used to fetch the repository, enabling authenticated git commands.

        :stability: experimental
        '''
        result = self._values.get("ssh_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_known_hosts(self) -> typing.Optional[builtins.str]:
        '''(experimental) Known hosts to add to the SSH configuration.

        Public SSH keys for a host can be obtained with ``ssh-keyscan``,
        e.g., ``ssh-keyscan github.com``.

        :stability: experimental
        '''
        result = self._values.get("ssh_known_hosts")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ssh_strict(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to perform strict host key checking.

        When ``true``, adds strict SSH configuration options to the command line.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("ssh_strict")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ssh_user(self) -> typing.Optional[builtins.str]:
        '''(experimental) User for connecting to the SSH host.

        Defaults to 'git'.

        :default: "git"

        :stability: experimental
        '''
        result = self._values.get("ssh_user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def submodules(self) -> typing.Optional[typing.Union[builtins.bool, builtins.str]]:
        '''(experimental) Whether to checkout submodules, with options for ``true`` (checkout submodules) or ``recursive`` (checkout submodules recursively).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("submodules")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, builtins.str]], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''(experimental) Personal Access Token (PAT) used to fetch the repository, enabling authenticated git commands.

        :default: github.token

        :stability: experimental
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckoutProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SetupNode(
    _Action_64902b3f,
    metaclass=jsii.JSIIMeta,
    jsii_type="github-actions-cdk.actions.SetupNode",
):
    '''(experimental) Class representing a Node.js setup action, allowing configuration of the Node.js version, registry settings, caching, and more within a GitHub Actions workflow.

    :stability: experimental
    '''

    def __init__(
        self,
        id: builtins.str,
        *,
        node_version: builtins.str,
        always_auth: typing.Optional[builtins.bool] = None,
        architecture: typing.Optional[builtins.str] = None,
        cache: typing.Optional[builtins.str] = None,
        cache_dependency_path: typing.Optional[builtins.str] = None,
        check_latest: typing.Optional[builtins.bool] = None,
        node_version_file: typing.Optional[builtins.str] = None,
        registry_url: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
        version: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Initializes a new instance of the ``SetupNode`` action.

        :param id: - A unique identifier for the action instance.
        :param node_version: (experimental) Version specification of Node.js to use in SemVer notation. Supports various aliases, such as ``lts/*`` for long-term support versions, as well as specific builds.
        :param always_auth: (experimental) Enables ``always-auth`` in the npmrc configuration to always require authentication. Default: false
        :param architecture: (experimental) Target system architecture for the Node.js installation.
        :param cache: (experimental) Specifies the package manager to use for caching dependencies in the default directory. Supported values include ``"npm"``, ``"yarn"``, and ``"pnpm"``.
        :param cache_dependency_path: (experimental) Path to the dependency file used for caching. Supports individual file paths and wildcards to match multiple files.
        :param check_latest: (experimental) When set to ``true``, checks for the latest available Node.js version that matches the specified version. Default: false
        :param node_version_file: (experimental) File containing the Node.js version specification, typically used by version managers.
        :param registry_url: (experimental) Optional URL of the registry for configuring authentication. This URL is used to set up a project-level ``.npmrc`` and ``.yarnrc`` file, allowing authentication through the ``NODE_AUTH_TOKEN`` environment variable.
        :param scope: (experimental) Optional scope for authentication against scoped registries. If unspecified, defaults to the repository owner when using GitHub Packages.
        :param token: (experimental) Token used to fetch Node.js distributions. Defaults to ``github.token`` on GitHub.com. For GitHub Enterprise Server (GHES), a personal access token may be used to avoid rate limiting. Default: github.server_url === "https://github.com" ? github.token : ""
        :param version: (experimental) The version of the action, can be a specific version, tag, or commit SHA.
        :param name: (experimental) Optional name for the action, displayed in logs.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96a773a8ea6370190838e1b94a9adacb9fd0845fda04353baac832189e61ac81)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SetupNodeProps(
            node_version=node_version,
            always_auth=always_auth,
            architecture=architecture,
            cache=cache,
            cache_dependency_path=cache_dependency_path,
            check_latest=check_latest,
            node_version_file=node_version_file,
            registry_url=registry_url,
            scope=scope,
            token=token,
            version=version,
            name=name,
        )

        jsii.create(self.__class__, self, [id, props])

    @jsii.member(jsii_name="bind")
    def bind(self, job: _Job_0ed15d61) -> _Step_edd90555:
        '''(experimental) Binds the action to a job by adding it as a step in the GitHub Actions workflow.

        This method configures the action's parameters and integrates it into the specified job,
        making it a part of the workflow execution.

        :param job: - The job to bind the action to.

        :return: The configured ``Step`` for the GitHub Actions job.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8992a7ed0c0a0f3d1063d790388fd2f1f6e1e83960980f67ed375cefeb6c9d3)
            check_type(argname="argument job", value=job, expected_type=type_hints["job"])
        return typing.cast(_Step_edd90555, jsii.invoke(self, "bind", [job]))

    @builtins.property
    @jsii.member(jsii_name="nodeVersion")
    def node_version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "nodeVersion"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> "SetupNodeOutputs":
        '''(experimental) Retrieves the outputs of the SetupNode action as specified in the GitHub Actions context.

        This method returns an object containing output values that can be referenced in subsequent
        steps of the workflow, such as the installed Node.js version and cache hit status.

        :return: An object containing the output values of the action.

        :stability: experimental
        '''
        return typing.cast("SetupNodeOutputs", jsii.get(self, "outputs"))

    @builtins.property
    @jsii.member(jsii_name="alwaysAuth")
    def always_auth(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "alwaysAuth"))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "architecture"))

    @builtins.property
    @jsii.member(jsii_name="cache")
    def cache(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cache"))

    @builtins.property
    @jsii.member(jsii_name="cacheDependencyPath")
    def cache_dependency_path(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cacheDependencyPath"))

    @builtins.property
    @jsii.member(jsii_name="checkLatest")
    def check_latest(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "checkLatest"))

    @builtins.property
    @jsii.member(jsii_name="nodeVersionFile")
    def node_version_file(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeVersionFile"))

    @builtins.property
    @jsii.member(jsii_name="registryUrl")
    def registry_url(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryUrl"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scope"))

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "token"))


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.SetupNodeOutputs",
    jsii_struct_bases=[],
    name_mapping={"cache_hit": "cacheHit", "node_version": "nodeVersion"},
)
class SetupNodeOutputs:
    def __init__(self, *, cache_hit: builtins.str, node_version: builtins.str) -> None:
        '''(experimental) Output structure for the Setup Node.js action.

        Extends from ActionOutputs to include specific outputs related to
        the Node.js setup process.

        :param cache_hit: (experimental) A boolean value represented as a string indicating if a cache was hit.
        :param node_version: (experimental) The version of Node.js that was installed.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8de0b51b0cf4372bb6ad7f6edaba90f950ae2ded4f8dc5a273c42627e3413597)
            check_type(argname="argument cache_hit", value=cache_hit, expected_type=type_hints["cache_hit"])
            check_type(argname="argument node_version", value=node_version, expected_type=type_hints["node_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cache_hit": cache_hit,
            "node_version": node_version,
        }

    @builtins.property
    def cache_hit(self) -> builtins.str:
        '''(experimental) A boolean value represented as a string indicating if a cache was hit.

        :stability: experimental
        '''
        result = self._values.get("cache_hit")
        assert result is not None, "Required property 'cache_hit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_version(self) -> builtins.str:
        '''(experimental) The version of Node.js that was installed.

        :stability: experimental
        '''
        result = self._values.get("node_version")
        assert result is not None, "Required property 'node_version' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SetupNodeOutputs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="github-actions-cdk.actions.SetupNodeProps",
    jsii_struct_bases=[_ActionProps_ebcddbbb],
    name_mapping={
        "version": "version",
        "name": "name",
        "node_version": "nodeVersion",
        "always_auth": "alwaysAuth",
        "architecture": "architecture",
        "cache": "cache",
        "cache_dependency_path": "cacheDependencyPath",
        "check_latest": "checkLatest",
        "node_version_file": "nodeVersionFile",
        "registry_url": "registryUrl",
        "scope": "scope",
        "token": "token",
    },
)
class SetupNodeProps(_ActionProps_ebcddbbb):
    def __init__(
        self,
        *,
        version: builtins.str,
        name: typing.Optional[builtins.str] = None,
        node_version: builtins.str,
        always_auth: typing.Optional[builtins.bool] = None,
        architecture: typing.Optional[builtins.str] = None,
        cache: typing.Optional[builtins.str] = None,
        cache_dependency_path: typing.Optional[builtins.str] = None,
        check_latest: typing.Optional[builtins.bool] = None,
        node_version_file: typing.Optional[builtins.str] = None,
        registry_url: typing.Optional[builtins.str] = None,
        scope: typing.Optional[builtins.str] = None,
        token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for configuring the Setup Node.js action in a GitHub Actions workflow.

        This interface extends ActionProps to include specific inputs for the
        Setup Node.js action, such as version specifications and authentication settings.

        :param version: (experimental) The version of the action, can be a specific version, tag, or commit SHA.
        :param name: (experimental) Optional name for the action, displayed in logs.
        :param node_version: (experimental) Version specification of Node.js to use in SemVer notation. Supports various aliases, such as ``lts/*`` for long-term support versions, as well as specific builds.
        :param always_auth: (experimental) Enables ``always-auth`` in the npmrc configuration to always require authentication. Default: false
        :param architecture: (experimental) Target system architecture for the Node.js installation.
        :param cache: (experimental) Specifies the package manager to use for caching dependencies in the default directory. Supported values include ``"npm"``, ``"yarn"``, and ``"pnpm"``.
        :param cache_dependency_path: (experimental) Path to the dependency file used for caching. Supports individual file paths and wildcards to match multiple files.
        :param check_latest: (experimental) When set to ``true``, checks for the latest available Node.js version that matches the specified version. Default: false
        :param node_version_file: (experimental) File containing the Node.js version specification, typically used by version managers.
        :param registry_url: (experimental) Optional URL of the registry for configuring authentication. This URL is used to set up a project-level ``.npmrc`` and ``.yarnrc`` file, allowing authentication through the ``NODE_AUTH_TOKEN`` environment variable.
        :param scope: (experimental) Optional scope for authentication against scoped registries. If unspecified, defaults to the repository owner when using GitHub Packages.
        :param token: (experimental) Token used to fetch Node.js distributions. Defaults to ``github.token`` on GitHub.com. For GitHub Enterprise Server (GHES), a personal access token may be used to avoid rate limiting. Default: github.server_url === "https://github.com" ? github.token : ""

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d0aa6275da72d1b188b10e139872a4e21efec2a154da533824d02864df5eff)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument node_version", value=node_version, expected_type=type_hints["node_version"])
            check_type(argname="argument always_auth", value=always_auth, expected_type=type_hints["always_auth"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument cache", value=cache, expected_type=type_hints["cache"])
            check_type(argname="argument cache_dependency_path", value=cache_dependency_path, expected_type=type_hints["cache_dependency_path"])
            check_type(argname="argument check_latest", value=check_latest, expected_type=type_hints["check_latest"])
            check_type(argname="argument node_version_file", value=node_version_file, expected_type=type_hints["node_version_file"])
            check_type(argname="argument registry_url", value=registry_url, expected_type=type_hints["registry_url"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "version": version,
            "node_version": node_version,
        }
        if name is not None:
            self._values["name"] = name
        if always_auth is not None:
            self._values["always_auth"] = always_auth
        if architecture is not None:
            self._values["architecture"] = architecture
        if cache is not None:
            self._values["cache"] = cache
        if cache_dependency_path is not None:
            self._values["cache_dependency_path"] = cache_dependency_path
        if check_latest is not None:
            self._values["check_latest"] = check_latest
        if node_version_file is not None:
            self._values["node_version_file"] = node_version_file
        if registry_url is not None:
            self._values["registry_url"] = registry_url
        if scope is not None:
            self._values["scope"] = scope
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def version(self) -> builtins.str:
        '''(experimental) The version of the action, can be a specific version, tag, or commit SHA.

        :stability: experimental

        Example::

            version: "v2"
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional name for the action, displayed in logs.

        :stability: experimental

        Example::

            "Checkout Repository"
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_version(self) -> builtins.str:
        '''(experimental) Version specification of Node.js to use in SemVer notation. Supports various aliases, such as ``lts/*`` for long-term support versions, as well as specific builds.

        :stability: experimental

        Example::

            "12.x", "10.15.1", ">=10.15.0", "lts/Hydrogen", "16-nightly", "latest", "node"
        '''
        result = self._values.get("node_version")
        assert result is not None, "Required property 'node_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def always_auth(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables ``always-auth`` in the npmrc configuration to always require authentication.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("always_auth")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''(experimental) Target system architecture for the Node.js installation.

        :stability: experimental

        Example::

            "x86" | "x64" - Defaults to the system architecture if not specified.
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the package manager to use for caching dependencies in the default directory.

        Supported values include ``"npm"``, ``"yarn"``, and ``"pnpm"``.

        :stability: experimental
        '''
        result = self._values.get("cache")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cache_dependency_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to the dependency file used for caching.

        Supports individual file paths and wildcards to match multiple files.

        :stability: experimental

        Example::

            "package-lock.json", "yarn.lock"
        '''
        result = self._values.get("cache_dependency_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def check_latest(self) -> typing.Optional[builtins.bool]:
        '''(experimental) When set to ``true``, checks for the latest available Node.js version that matches the specified version.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("check_latest")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def node_version_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) File containing the Node.js version specification, typically used by version managers.

        :stability: experimental

        Example::

            "package.json", ".nvmrc", ".node-version", ".tool-versions"
        '''
        result = self._values.get("node_version_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional URL of the registry for configuring authentication.

        This URL is used to set up a project-level
        ``.npmrc`` and ``.yarnrc`` file, allowing authentication through the ``NODE_AUTH_TOKEN`` environment variable.

        :stability: experimental
        '''
        result = self._values.get("registry_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional scope for authentication against scoped registries.

        If unspecified,
        defaults to the repository owner when using GitHub Packages.

        :stability: experimental
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token(self) -> typing.Optional[builtins.str]:
        '''(experimental) Token used to fetch Node.js distributions. Defaults to ``github.token`` on GitHub.com. For GitHub Enterprise Server (GHES), a personal access token may be used to avoid rate limiting.

        :default: github.server_url === "https://github.com" ? github.token : ""

        :stability: experimental
        '''
        result = self._values.get("token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SetupNodeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Checkout",
    "CheckoutOutputs",
    "CheckoutProps",
    "SetupNode",
    "SetupNodeOutputs",
    "SetupNodeProps",
]

publication.publish()

def _typecheckingstub__1830fde06e0939430f30c3b1ec33ce537d1db25383e2ed028b1573eec5580451(
    id: builtins.str,
    *,
    clean: typing.Optional[builtins.bool] = None,
    fetch_depth: typing.Optional[jsii.Number] = None,
    fetch_tags: typing.Optional[builtins.bool] = None,
    filter: typing.Optional[builtins.str] = None,
    github_server_url: typing.Optional[builtins.str] = None,
    lfs: typing.Optional[builtins.bool] = None,
    path: typing.Optional[builtins.str] = None,
    persist_credentials: typing.Optional[builtins.bool] = None,
    ref: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    set_safe_directory: typing.Optional[builtins.bool] = None,
    show_progress: typing.Optional[builtins.bool] = None,
    sparse_checkout: typing.Optional[typing.Sequence[builtins.str]] = None,
    sparse_checkout_cone_mode: typing.Optional[builtins.bool] = None,
    ssh_key: typing.Optional[builtins.str] = None,
    ssh_known_hosts: typing.Optional[builtins.str] = None,
    ssh_strict: typing.Optional[builtins.bool] = None,
    ssh_user: typing.Optional[builtins.str] = None,
    submodules: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
    token: typing.Optional[builtins.str] = None,
    version: builtins.str,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f0a73ca3133b853cf44ee1014c16c956601bc137b20a8eba70009e9702ec37(
    job: _Job_0ed15d61,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338965b7fbb099ee70e062ffce8e483fd1fa0e4c884043df4b017a6beed355f1(
    *,
    commit: builtins.str,
    ref: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbc9a9372aa10e00b2ff916f92a8052e93e51aa4a2ea16b98140884c5a72b662(
    *,
    version: builtins.str,
    name: typing.Optional[builtins.str] = None,
    clean: typing.Optional[builtins.bool] = None,
    fetch_depth: typing.Optional[jsii.Number] = None,
    fetch_tags: typing.Optional[builtins.bool] = None,
    filter: typing.Optional[builtins.str] = None,
    github_server_url: typing.Optional[builtins.str] = None,
    lfs: typing.Optional[builtins.bool] = None,
    path: typing.Optional[builtins.str] = None,
    persist_credentials: typing.Optional[builtins.bool] = None,
    ref: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    set_safe_directory: typing.Optional[builtins.bool] = None,
    show_progress: typing.Optional[builtins.bool] = None,
    sparse_checkout: typing.Optional[typing.Sequence[builtins.str]] = None,
    sparse_checkout_cone_mode: typing.Optional[builtins.bool] = None,
    ssh_key: typing.Optional[builtins.str] = None,
    ssh_known_hosts: typing.Optional[builtins.str] = None,
    ssh_strict: typing.Optional[builtins.bool] = None,
    ssh_user: typing.Optional[builtins.str] = None,
    submodules: typing.Optional[typing.Union[builtins.bool, builtins.str]] = None,
    token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96a773a8ea6370190838e1b94a9adacb9fd0845fda04353baac832189e61ac81(
    id: builtins.str,
    *,
    node_version: builtins.str,
    always_auth: typing.Optional[builtins.bool] = None,
    architecture: typing.Optional[builtins.str] = None,
    cache: typing.Optional[builtins.str] = None,
    cache_dependency_path: typing.Optional[builtins.str] = None,
    check_latest: typing.Optional[builtins.bool] = None,
    node_version_file: typing.Optional[builtins.str] = None,
    registry_url: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
    version: builtins.str,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8992a7ed0c0a0f3d1063d790388fd2f1f6e1e83960980f67ed375cefeb6c9d3(
    job: _Job_0ed15d61,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de0b51b0cf4372bb6ad7f6edaba90f950ae2ded4f8dc5a273c42627e3413597(
    *,
    cache_hit: builtins.str,
    node_version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d0aa6275da72d1b188b10e139872a4e21efec2a154da533824d02864df5eff(
    *,
    version: builtins.str,
    name: typing.Optional[builtins.str] = None,
    node_version: builtins.str,
    always_auth: typing.Optional[builtins.bool] = None,
    architecture: typing.Optional[builtins.str] = None,
    cache: typing.Optional[builtins.str] = None,
    cache_dependency_path: typing.Optional[builtins.str] = None,
    check_latest: typing.Optional[builtins.bool] = None,
    node_version_file: typing.Optional[builtins.str] = None,
    registry_url: typing.Optional[builtins.str] = None,
    scope: typing.Optional[builtins.str] = None,
    token: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
