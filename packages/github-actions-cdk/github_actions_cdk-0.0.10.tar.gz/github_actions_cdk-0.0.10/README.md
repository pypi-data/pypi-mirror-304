# 🚧 GitHub Actions CDK

**github-actions-cdk** is a TypeScript library that simplifies the creation and management of GitHub Actions workflows using Constructs. With this library, developers can define workflows in a structured and type-safe manner, making it easier to automate CI/CD pipelines on GitHub.

## Features

* **Type-Safe Workflows**: Leverage TypeScript's strong typing to define your GitHub Actions workflows and ensure correctness.
* **Modular Design**: Easily create and manage jobs, triggers, and options for your workflows.
* **Built-In Support for GitHub Events**: Configure workflows based on various GitHub events such as push, pull request, issue comments, and more.
* **Customizable Options**: Define environment variables, permissions, concurrency settings, and default job settings.

## Installation

To get started with `github-actions-cdk`, install the package using npm or yarn:

```bash
npm install github-actions-cdk
```

or

```bash
yarn add github-actions-cdk
```

## Getting Started

### Basic Usage

Here's a simple example of how to create a GitHub Actions workflow using `github-actions-cdk`:

```python
import { PermissionLevel, Project } from 'github-actions-cdk';
import { Checkout, SetupNode } from 'github-actions-cdk/actions';

const project = new Project();

const workflow = project.addWorkflow('build', {
    name: "Build",
    triggers: {
        push: { branches: ['main'] },
        workflowDispatch: {}
    },
    permissions: {
        contents: PermissionLevel.READ,
    }
});

const job = workflow.addJob('build', {
	env: {
		CI: 'true',
	},
});

job.addAction(
  new Checkout("checkout", {
    name: "Checkout Code",
    version: "v4",
  }),
);

job.addAction(
  new SetupNode("setup-node", {
    name: "Set up Node.js",
    version: "v4",
    nodeVersion: "20.x",
  }),
);

project.synth();
```

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING.md](./CONTRIBUTING.md) for details on how to get involved.

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENCE) file for more information.
