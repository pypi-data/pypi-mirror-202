'''
# Astro Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Introduction

[Astro](https://astro.build/) is the all-in-one web framework designed for speed. This library is supported modes, `static`, `lambda` and `edge`, to deploy astro website to AWS.

## Architecture

### Static

![static](https://raw.githubusercontent.com/helbing/astrojs-aws/main/docs/static/architecture/static.png)

### Lambda

![lambda](https://raw.githubusercontent.com/helbing/astrojs-aws/main/docs/static/architecture/lambda.png)

### Edge

![edge](https://raw.githubusercontent.com/helbing/astrojs-aws/main/docs/static/architecture/edge.png)

## Static Mode

```python
site = astrojsaws.StaticAstroSite(self, "AstroSite",
    static_dir="/path/to/dist"
)
```

## Lambda Mode

```python
site = astrojsaws.LambdaAstroSite(self, "AstroSite",
    server_entry="/path/to/dist/server/entry.mjs",
    static_dir="/path/to/dist/client"
)
```

## Edge Mode

```python
site = astrojsaws.EdgeAstroSite(self, "AstroSite",
    server_entry="/path/to/dist/server/entry.mjs",
    static_dir="/path/to/dist/client"
)
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_apigatewayv2_alpha as _aws_cdk_aws_apigatewayv2_alpha_050969fe
import aws_cdk.aws_certificatemanager as _aws_cdk_aws_certificatemanager_ceddda9d
import aws_cdk.aws_cloudfront as _aws_cdk_aws_cloudfront_ceddda9d
import aws_cdk.aws_cloudfront_origins as _aws_cdk_aws_cloudfront_origins_ceddda9d
import aws_cdk.aws_codeguruprofiler as _aws_cdk_aws_codeguruprofiler_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_lambda_nodejs as _aws_cdk_aws_lambda_nodejs_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d
import constructs as _constructs_77d1e7e8


class AstroSiteConstruct(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@astrojs-aws/construct.AstroSiteConstruct",
):
    '''(experimental) The base class for all constructs.

    :stability: experimental
    '''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db9d982b9095784bc59520b993f10dfaad2bbd6ee2cb8c80aa143a1c8c6d25a8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])

    @jsii.member(jsii_name="newBucket")
    def new_bucket(
        self,
        scope: _constructs_77d1e7e8.Construct,
        static_dir: builtins.str,
        *,
        access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
        auto_delete_objects: typing.Optional[builtins.bool] = None,
        block_public_access: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BlockPublicAccess] = None,
        bucket_key_enabled: typing.Optional[builtins.bool] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        enforce_ssl: typing.Optional[builtins.bool] = None,
        event_bridge_enabled: typing.Optional[builtins.bool] = None,
        intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.IntelligentTieringConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
        inventories: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.Inventory, typing.Dict[builtins.str, typing.Any]]]] = None,
        lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        metrics: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketMetrics, typing.Dict[builtins.str, typing.Any]]]] = None,
        notifications_handler_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        object_lock_default_retention: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectLockRetention] = None,
        object_lock_enabled: typing.Optional[builtins.bool] = None,
        object_ownership: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectOwnership] = None,
        public_read_access: typing.Optional[builtins.bool] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        server_access_logs_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        server_access_logs_prefix: typing.Optional[builtins.str] = None,
        transfer_acceleration: typing.Optional[builtins.bool] = None,
        versioned: typing.Optional[builtins.bool] = None,
        website_error_document: typing.Optional[builtins.str] = None,
        website_index_document: typing.Optional[builtins.str] = None,
        website_redirect: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.RedirectTarget, typing.Dict[builtins.str, typing.Any]]] = None,
        website_routing_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.RoutingRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> _aws_cdk_aws_s3_ceddda9d.Bucket:
        '''(experimental) New bucket.

        :param scope: -
        :param static_dir: -
        :param access_control: Specifies a canned ACL that grants predefined permissions to the bucket. Default: BucketAccessControl.PRIVATE
        :param auto_delete_objects: Whether all objects should be automatically deleted when the bucket is removed from the stack or when the stack is deleted. Requires the ``removalPolicy`` to be set to ``RemovalPolicy.DESTROY``. **Warning** if you have deployed a bucket with ``autoDeleteObjects: true``, switching this to ``false`` in a CDK version *before* ``1.126.0`` will lead to all objects in the bucket being deleted. Be sure to update your bucket resources by deploying with CDK version ``1.126.0`` or later **before** switching this value to ``false``. Default: false
        :param block_public_access: The block public access configuration of this bucket. Default: - CloudFormation defaults will apply. New buckets and objects don't allow public access, but users can modify bucket policies or object permissions to allow public access
        :param bucket_key_enabled: Whether Amazon S3 should use its own intermediary key to generate data keys. Only relevant when using KMS for encryption. - If not enabled, every object GET and PUT will cause an API call to KMS (with the attendant cost implications of that). - If enabled, S3 will use its own time-limited key instead. Only relevant, when Encryption is set to ``BucketEncryption.KMS`` or ``BucketEncryption.KMS_MANAGED``. Default: - false
        :param bucket_name: Physical name of this bucket. Default: - Assigned by CloudFormation (recommended).
        :param cors: The CORS configuration of this bucket. Default: - No CORS configuration.
        :param encryption: The kind of server-side encryption to apply to this bucket. If you choose KMS, you can specify a KMS key via ``encryptionKey``. If encryption key is not specified, a key will automatically be created. Default: - ``Kms`` if ``encryptionKey`` is specified, or ``Unencrypted`` otherwise.
        :param encryption_key: External KMS key to use for bucket encryption. The 'encryption' property must be either not specified or set to "Kms". An error will be emitted if encryption is set to "Unencrypted" or "Managed". Default: - If encryption is set to "Kms" and this property is undefined, a new KMS key will be created and associated with this bucket.
        :param enforce_ssl: Enforces SSL for requests. S3.5 of the AWS Foundational Security Best Practices Regarding S3. Default: false
        :param event_bridge_enabled: Whether this bucket should send notifications to Amazon EventBridge or not. Default: false
        :param intelligent_tiering_configurations: Inteligent Tiering Configurations. Default: No Intelligent Tiiering Configurations.
        :param inventories: The inventory configuration of the bucket. Default: - No inventory configuration
        :param lifecycle_rules: Rules that define how Amazon S3 manages objects during their lifetime. Default: - No lifecycle rules.
        :param metrics: The metrics configuration of this bucket. Default: - No metrics configuration.
        :param notifications_handler_role: The role to be used by the notifications handler. Default: - a new role will be created.
        :param object_lock_default_retention: The default retention mode and rules for S3 Object Lock. Default retention can be configured after a bucket is created if the bucket already has object lock enabled. Enabling object lock for existing buckets is not supported. Default: no default retention period
        :param object_lock_enabled: Enable object lock on the bucket. Enabling object lock for existing buckets is not supported. Object lock must be enabled when the bucket is created. Default: false, unless objectLockDefaultRetention is set (then, true)
        :param object_ownership: The objectOwnership of the bucket. Default: - No ObjectOwnership configuration, uploading account will own the object.
        :param public_read_access: Grants public read access to all objects in the bucket. Similar to calling ``bucket.grantPublicAccess()`` Default: false
        :param removal_policy: Policy to apply when the bucket is removed from this stack. Default: - The bucket will be orphaned.
        :param server_access_logs_bucket: Destination bucket for the server access logs. Default: - If "serverAccessLogsPrefix" undefined - access logs disabled, otherwise - log to current bucket.
        :param server_access_logs_prefix: Optional log file prefix to use for the bucket's access logs. If defined without "serverAccessLogsBucket", enables access logs to current bucket with this prefix. Default: - No log file prefix
        :param transfer_acceleration: Whether this bucket should have transfer acceleration turned on or not. Default: false
        :param versioned: Whether this bucket should have versioning turned on or not. Default: false (unless object lock is enabled, then true)
        :param website_error_document: The name of the error document (e.g. "404.html") for the website. ``websiteIndexDocument`` must also be set if this is set. Default: - No error document.
        :param website_index_document: The name of the index document (e.g. "index.html") for the website. Enables static website hosting for this bucket. Default: - No index document.
        :param website_redirect: Specifies the redirect behavior of all requests to a website endpoint of a bucket. If you specify this property, you can't specify "websiteIndexDocument", "websiteErrorDocument" nor , "websiteRoutingRules". Default: - No redirection.
        :param website_routing_rules: Rules that define when a redirect is applied and the redirect behavior. Default: - No redirection rules.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a04f0b61812d848db8d60a2935ebfc24eb9b442dc947ccedced2b672fafbcbb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument static_dir", value=static_dir, expected_type=type_hints["static_dir"])
        props = _aws_cdk_aws_s3_ceddda9d.BucketProps(
            access_control=access_control,
            auto_delete_objects=auto_delete_objects,
            block_public_access=block_public_access,
            bucket_key_enabled=bucket_key_enabled,
            bucket_name=bucket_name,
            cors=cors,
            encryption=encryption,
            encryption_key=encryption_key,
            enforce_ssl=enforce_ssl,
            event_bridge_enabled=event_bridge_enabled,
            intelligent_tiering_configurations=intelligent_tiering_configurations,
            inventories=inventories,
            lifecycle_rules=lifecycle_rules,
            metrics=metrics,
            notifications_handler_role=notifications_handler_role,
            object_lock_default_retention=object_lock_default_retention,
            object_lock_enabled=object_lock_enabled,
            object_ownership=object_ownership,
            public_read_access=public_read_access,
            removal_policy=removal_policy,
            server_access_logs_bucket=server_access_logs_bucket,
            server_access_logs_prefix=server_access_logs_prefix,
            transfer_acceleration=transfer_acceleration,
            versioned=versioned,
            website_error_document=website_error_document,
            website_index_document=website_index_document,
            website_redirect=website_redirect,
            website_routing_rules=website_routing_rules,
        )

        return typing.cast(_aws_cdk_aws_s3_ceddda9d.Bucket, jsii.invoke(self, "newBucket", [scope, static_dir, props]))

    @jsii.member(jsii_name="newFunction")
    def new_function(
        self,
        scope: _constructs_77d1e7e8.Construct,
        server_entry: builtins.str,
        *,
        bundling: typing.Optional[typing.Union[_aws_cdk_aws_lambda_nodejs_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        runtime: typing.Optional[builtins.str] = None,
        adot_instrumentation: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
        code_signing_config: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig] = None,
        current_version_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.VersionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
        dead_letter_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        events: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.IEventSource]] = None,
        filesystem: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem] = None,
        function_name: typing.Optional[builtins.str] = None,
        initial_policy: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
        insights_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion] = None,
        layers: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        profiling: typing.Optional[builtins.bool] = None,
        profiling_group: typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        runtime_management_mode: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        tracing: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        on_failure: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        on_success: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> _aws_cdk_aws_lambda_nodejs_ceddda9d.NodejsFunction:
        '''(experimental) New nodejs function.

        :param scope: -
        :param server_entry: -
        :param bundling: (experimental) Bundling options.
        :param runtime: (experimental) The Nodejs Runtime. Default: nodejs18.x
        :param adot_instrumentation: Specify the configuration of AWS Distro for OpenTelemetry (ADOT) instrumentation. Default: - No ADOT instrumentation
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param allow_public_subnet: Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param architecture: The system architectures compatible with this lambda function. Default: Architecture.X86_64
        :param code_signing_config: Code signing config associated with this function. Default: - Not Sign the Code
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. If SNS topic is desired, specify ``deadLetterTopic`` property instead. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param dead_letter_topic: The SNS topic to use as a DLQ. Note that if ``deadLetterQueueEnabled`` is set to ``true``, an SQS queue will be created rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly. Default: - no SNS topic
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param environment_encryption: The AWS KMS key that's used to encrypt your function's environment variables. Default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        :param ephemeral_storage_size: The size of the function’s /tmp directory in MiB. Default: 512 MiB
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param insights_version: Specify the version of CloudWatch Lambda insights to use for monitoring. Default: - No Lambda Insights
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by multiple functions. Default: - No layers.
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param profiling: Enable profiling. Default: - No profiling.
        :param profiling_group: Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param runtime_management_mode: Sets the runtime management configuration for a function's version. Default: Auto
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. This is required when ``vpcSubnets`` is specified. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. This requires ``vpc`` to be specified in order for interfaces to actually be placed in the subnets. If ``vpc`` is not specify, this will raise an error. Note: Internet access for Lambda Functions requires a NAT Gateway, so picking public subnets is not allowed (unless ``allowPublicSubnet`` is set to ``true``). Default: - the Vpc default strategy if not specified
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80ed10c38699730e2bf5e69ee0bd4925e438d4799a5852709f308f2affea6d7f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument server_entry", value=server_entry, expected_type=type_hints["server_entry"])
        props = ServerOptions(
            bundling=bundling,
            runtime=runtime,
            adot_instrumentation=adot_instrumentation,
            allow_all_outbound=allow_all_outbound,
            allow_public_subnet=allow_public_subnet,
            architecture=architecture,
            code_signing_config=code_signing_config,
            current_version_options=current_version_options,
            dead_letter_queue=dead_letter_queue,
            dead_letter_queue_enabled=dead_letter_queue_enabled,
            dead_letter_topic=dead_letter_topic,
            description=description,
            environment=environment,
            environment_encryption=environment_encryption,
            ephemeral_storage_size=ephemeral_storage_size,
            events=events,
            filesystem=filesystem,
            function_name=function_name,
            initial_policy=initial_policy,
            insights_version=insights_version,
            layers=layers,
            log_retention=log_retention,
            log_retention_retry_options=log_retention_retry_options,
            log_retention_role=log_retention_role,
            memory_size=memory_size,
            profiling=profiling,
            profiling_group=profiling_group,
            reserved_concurrent_executions=reserved_concurrent_executions,
            role=role,
            runtime_management_mode=runtime_management_mode,
            security_groups=security_groups,
            timeout=timeout,
            tracing=tracing,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            max_event_age=max_event_age,
            on_failure=on_failure,
            on_success=on_success,
            retry_attempts=retry_attempts,
        )

        return typing.cast(_aws_cdk_aws_lambda_nodejs_ceddda9d.NodejsFunction, jsii.invoke(self, "newFunction", [scope, server_entry, props]))

    @jsii.member(jsii_name="newS3Origin")
    def new_s3_origin(
        self,
        scope: _constructs_77d1e7e8.Construct,
        bucket: _aws_cdk_aws_s3_ceddda9d.Bucket,
    ) -> _aws_cdk_aws_cloudfront_origins_ceddda9d.S3Origin:
        '''(experimental) New S3 origin.

        :param scope: -
        :param bucket: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b421adfa617ab976e8d23db7cc054c672a89b03727bc8aea382f4f4d5f4fef2e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        return typing.cast(_aws_cdk_aws_cloudfront_origins_ceddda9d.S3Origin, jsii.invoke(self, "newS3Origin", [scope, bucket]))

    @jsii.member(jsii_name="parseRoutesFromDir")
    def parse_routes_from_dir(self, dir: builtins.str) -> typing.List[builtins.str]:
        '''(experimental) Parse routes from directory if the item is directory will parse to /item/* if the item is file will parse to /item.

        :param dir: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf3fb2a8029aa3b0236943223b8d34ab2cc4770d3bfaa828c426b76ea51d6cd)
            check_type(argname="argument dir", value=dir, expected_type=type_hints["dir"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "parseRoutesFromDir", [dir]))

    @jsii.member(jsii_name="strToRuntime")
    def str_to_runtime(
        self,
        str: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_lambda_ceddda9d.Runtime:
        '''(experimental) Transform string to Runtime.

        :param str: -

        :default: Runtime.NODEJS_18_X

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce4b161f41068601e658dcd2dbe5f267f30e7aa75918596cd3c3a81973920c1)
            check_type(argname="argument str", value=str, expected_type=type_hints["str"])
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.Runtime, jsii.invoke(self, "strToRuntime", [str]))


@jsii.data_type(
    jsii_type="@astrojs-aws/construct.DistributionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "additional_behaviors": "additionalBehaviors",
        "certificate": "certificate",
        "comment": "comment",
        "domain_names": "domainNames",
        "enabled": "enabled",
        "enable_ipv6": "enableIpv6",
        "enable_logging": "enableLogging",
        "error_responses": "errorResponses",
        "geo_restriction": "geoRestriction",
        "http_version": "httpVersion",
        "log_bucket": "logBucket",
        "log_file_prefix": "logFilePrefix",
        "log_includes_cookies": "logIncludesCookies",
        "minimum_protocol_version": "minimumProtocolVersion",
        "price_class": "priceClass",
        "ssl_support_method": "sslSupportMethod",
        "web_acl_id": "webAclId",
    },
)
class DistributionOptions:
    def __init__(
        self,
        *,
        additional_behaviors: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
        comment: typing.Optional[builtins.str] = None,
        domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        enable_ipv6: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        error_responses: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse, typing.Dict[builtins.str, typing.Any]]]] = None,
        geo_restriction: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction] = None,
        http_version: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion] = None,
        log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        log_file_prefix: typing.Optional[builtins.str] = None,
        log_includes_cookies: typing.Optional[builtins.bool] = None,
        minimum_protocol_version: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SecurityPolicyProtocol] = None,
        price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
        ssl_support_method: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SSLMethod] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) CloudFront distribution which is based on CDK DistributionProps, remove defaultBehavior, defaultRootObject.

        :param additional_behaviors: (experimental) Additional behaviors for the distribution, mapped by the pathPattern that specifies which requests to apply the behavior to. Default: - no additional behaviors are added.
        :param certificate: (experimental) A certificate to associate with the distribution. The certificate must be located in N. Virginia (us-east-1). Default: - the CloudFront wildcard certificate (*.cloudfront.net) will be used.
        :param comment: (experimental) Any comments you want to include about the distribution. Default: - no comment
        :param domain_names: (experimental) Alternative domain names for this distribution. If you want to use your own domain name, such as www.example.com, instead of the cloudfront.net domain name, you can add an alternate domain name to your distribution. If you attach a certificate to the distribution, you must add (at least one of) the domain names of the certificate to this list. Default: - The distribution will only support the default generated name (e.g., d111111abcdef8.cloudfront.net)
        :param enabled: (experimental) Enable or disable the distribution. Default: true
        :param enable_ipv6: (experimental) Whether CloudFront will respond to IPv6 DNS requests with an IPv6 address. If you specify false, CloudFront responds to IPv6 DNS requests with the DNS response code NOERROR and with no IP addresses. This allows viewers to submit a second request, for an IPv4 address for your distribution. Default: true
        :param enable_logging: (experimental) Enable access logging for the distribution. Default: - false, unless ``logBucket`` is specified.
        :param error_responses: (experimental) How CloudFront should handle requests that are not successful (e.g., PageNotFound). Default: - No custom error responses.
        :param geo_restriction: (experimental) Controls the countries in which your content is distributed. Default: - No geographic restrictions
        :param http_version: (experimental) Specify the maximum HTTP version that you want viewers to use to communicate with CloudFront. For viewers and CloudFront to use HTTP/2, viewers must support TLS 1.2 or later, and must support server name identification (SNI). Default: HttpVersion.HTTP2
        :param log_bucket: (experimental) The Amazon S3 bucket to store the access logs in. Default: - A bucket is created if ``enableLogging`` is true
        :param log_file_prefix: (experimental) An optional string that you want CloudFront to prefix to the access log filenames for this distribution. Default: - no prefix
        :param log_includes_cookies: (experimental) Specifies whether you want CloudFront to include cookies in access logs. Default: false
        :param minimum_protocol_version: (experimental) The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections. CloudFront serves your objects only to browsers or devices that support at least the SSL version that you specify. Default: - SecurityPolicyProtocol.TLS_V1_2_2021 if the '
        :param price_class: (experimental) The price class that corresponds with the maximum price that you want to pay for CloudFront service. If you specify PriceClass_All, CloudFront responds to requests for your objects from all CloudFront edge locations. If you specify a price class other than PriceClass_All, CloudFront serves your objects from the CloudFront edge location that has the lowest latency among the edge locations in your price class. Default: PriceClass.PRICE_CLASS_ALL
        :param ssl_support_method: (experimental) The SSL method CloudFront will use for your distribution. Server Name Indication (SNI) - is an extension to the TLS computer networking protocol by which a client indicates which hostname it is attempting to connect to at the start of the handshaking process. This allows a server to present multiple certificates on the same IP address and TCP port number and hence allows multiple secure (HTTPS) websites (or any other service over TLS) to be served by the same IP address without requiring all those sites to use the same certificate. CloudFront can use SNI to host multiple distributions on the same IP - which a large majority of clients will support. If your clients cannot support SNI however - CloudFront can use dedicated IPs for your distribution - but there is a prorated monthly charge for using this feature. By default, we use SNI - but you can optionally enable dedicated IPs (VIP). See the CloudFront SSL for more details about pricing : https://aws.amazon.com/cloudfront/custom-ssl-domains/ Default: SSLMethod.SNI
        :param web_acl_id: (experimental) Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution. To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``. To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``. Default: - No AWS Web Application Firewall web access control list (web ACL).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d74a8a4e0de802e6bca8967c29913a63486c9eb1716556f1cb7e8757dc87a7ed)
            check_type(argname="argument additional_behaviors", value=additional_behaviors, expected_type=type_hints["additional_behaviors"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument domain_names", value=domain_names, expected_type=type_hints["domain_names"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument enable_ipv6", value=enable_ipv6, expected_type=type_hints["enable_ipv6"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument error_responses", value=error_responses, expected_type=type_hints["error_responses"])
            check_type(argname="argument geo_restriction", value=geo_restriction, expected_type=type_hints["geo_restriction"])
            check_type(argname="argument http_version", value=http_version, expected_type=type_hints["http_version"])
            check_type(argname="argument log_bucket", value=log_bucket, expected_type=type_hints["log_bucket"])
            check_type(argname="argument log_file_prefix", value=log_file_prefix, expected_type=type_hints["log_file_prefix"])
            check_type(argname="argument log_includes_cookies", value=log_includes_cookies, expected_type=type_hints["log_includes_cookies"])
            check_type(argname="argument minimum_protocol_version", value=minimum_protocol_version, expected_type=type_hints["minimum_protocol_version"])
            check_type(argname="argument price_class", value=price_class, expected_type=type_hints["price_class"])
            check_type(argname="argument ssl_support_method", value=ssl_support_method, expected_type=type_hints["ssl_support_method"])
            check_type(argname="argument web_acl_id", value=web_acl_id, expected_type=type_hints["web_acl_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if additional_behaviors is not None:
            self._values["additional_behaviors"] = additional_behaviors
        if certificate is not None:
            self._values["certificate"] = certificate
        if comment is not None:
            self._values["comment"] = comment
        if domain_names is not None:
            self._values["domain_names"] = domain_names
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_ipv6 is not None:
            self._values["enable_ipv6"] = enable_ipv6
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if error_responses is not None:
            self._values["error_responses"] = error_responses
        if geo_restriction is not None:
            self._values["geo_restriction"] = geo_restriction
        if http_version is not None:
            self._values["http_version"] = http_version
        if log_bucket is not None:
            self._values["log_bucket"] = log_bucket
        if log_file_prefix is not None:
            self._values["log_file_prefix"] = log_file_prefix
        if log_includes_cookies is not None:
            self._values["log_includes_cookies"] = log_includes_cookies
        if minimum_protocol_version is not None:
            self._values["minimum_protocol_version"] = minimum_protocol_version
        if price_class is not None:
            self._values["price_class"] = price_class
        if ssl_support_method is not None:
            self._values["ssl_support_method"] = ssl_support_method
        if web_acl_id is not None:
            self._values["web_acl_id"] = web_acl_id

    @builtins.property
    def additional_behaviors(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions]]:
        '''(experimental) Additional behaviors for the distribution, mapped by the pathPattern that specifies which requests to apply the behavior to.

        :default: - no additional behaviors are added.

        :stability: experimental
        '''
        result = self._values.get("additional_behaviors")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions]], result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]:
        '''(experimental) A certificate to associate with the distribution.

        The certificate must be located in N. Virginia (us-east-1).

        :default: - the CloudFront wildcard certificate (*.cloudfront.net) will be used.

        :stability: experimental
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''(experimental) Any comments you want to include about the distribution.

        :default: - no comment

        :stability: experimental
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domain_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Alternative domain names for this distribution.

        If you want to use your own domain name, such as www.example.com, instead of the cloudfront.net domain name,
        you can add an alternate domain name to your distribution. If you attach a certificate to the distribution,
        you must add (at least one of) the domain names of the certificate to this list.

        :default: - The distribution will only support the default generated name (e.g., d111111abcdef8.cloudfront.net)

        :stability: experimental
        '''
        result = self._values.get("domain_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable or disable the distribution.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_ipv6(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether CloudFront will respond to IPv6 DNS requests with an IPv6 address.

        If you specify false, CloudFront responds to IPv6 DNS requests with the DNS response code NOERROR and with no IP addresses.
        This allows viewers to submit a second request, for an IPv4 address for your distribution.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enable_ipv6")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable access logging for the distribution.

        :default: - false, unless ``logBucket`` is specified.

        :stability: experimental
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def error_responses(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse]]:
        '''(experimental) How CloudFront should handle requests that are not successful (e.g., PageNotFound).

        :default: - No custom error responses.

        :stability: experimental
        '''
        result = self._values.get("error_responses")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse]], result)

    @builtins.property
    def geo_restriction(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction]:
        '''(experimental) Controls the countries in which your content is distributed.

        :default: - No geographic restrictions

        :stability: experimental
        '''
        result = self._values.get("geo_restriction")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction], result)

    @builtins.property
    def http_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion]:
        '''(experimental) Specify the maximum HTTP version that you want viewers to use to communicate with CloudFront.

        For viewers and CloudFront to use HTTP/2, viewers must support TLS 1.2 or later, and must support server name identification (SNI).

        :default: HttpVersion.HTTP2

        :stability: experimental
        '''
        result = self._values.get("http_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion], result)

    @builtins.property
    def log_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''(experimental) The Amazon S3 bucket to store the access logs in.

        :default: - A bucket is created if ``enableLogging`` is true

        :stability: experimental
        '''
        result = self._values.get("log_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def log_file_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) An optional string that you want CloudFront to prefix to the access log filenames for this distribution.

        :default: - no prefix

        :stability: experimental
        '''
        result = self._values.get("log_file_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_includes_cookies(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether you want CloudFront to include cookies in access logs.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("log_includes_cookies")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minimum_protocol_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SecurityPolicyProtocol]:
        '''(experimental) The minimum version of the SSL protocol that you want CloudFront to use for HTTPS connections.

        CloudFront serves your objects only to browsers or devices that support at
        least the SSL version that you specify.

        :default: - SecurityPolicyProtocol.TLS_V1_2_2021 if the '

        :stability: experimental
        :aws-cdk: /aws-cloudfront:defaultSecurityPolicyTLSv1.2_2021' feature flag is set; otherwise, SecurityPolicyProtocol.TLS_V1_2_2019.
        '''
        result = self._values.get("minimum_protocol_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SecurityPolicyProtocol], result)

    @builtins.property
    def price_class(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass]:
        '''(experimental) The price class that corresponds with the maximum price that you want to pay for CloudFront service.

        If you specify PriceClass_All, CloudFront responds to requests for your objects from all CloudFront edge locations.
        If you specify a price class other than PriceClass_All, CloudFront serves your objects from the CloudFront edge location
        that has the lowest latency among the edge locations in your price class.

        :default: PriceClass.PRICE_CLASS_ALL

        :stability: experimental
        '''
        result = self._values.get("price_class")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass], result)

    @builtins.property
    def ssl_support_method(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SSLMethod]:
        '''(experimental) The SSL method CloudFront will use for your distribution.

        Server Name Indication (SNI) - is an extension to the TLS computer networking protocol by which a client indicates
        which hostname it is attempting to connect to at the start of the handshaking process. This allows a server to present
        multiple certificates on the same IP address and TCP port number and hence allows multiple secure (HTTPS) websites
        (or any other service over TLS) to be served by the same IP address without requiring all those sites to use the same certificate.

        CloudFront can use SNI to host multiple distributions on the same IP - which a large majority of clients will support.

        If your clients cannot support SNI however - CloudFront can use dedicated IPs for your distribution - but there is a prorated monthly charge for
        using this feature. By default, we use SNI - but you can optionally enable dedicated IPs (VIP).

        See the CloudFront SSL for more details about pricing : https://aws.amazon.com/cloudfront/custom-ssl-domains/

        :default: SSLMethod.SNI

        :stability: experimental
        '''
        result = self._values.get("ssl_support_method")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SSLMethod], result)

    @builtins.property
    def web_acl_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Unique identifier that specifies the AWS WAF web ACL to associate with this CloudFront distribution.

        To specify a web ACL created using the latest version of AWS WAF, use the ACL ARN, for example
        ``arn:aws:wafv2:us-east-1:123456789012:global/webacl/ExampleWebACL/473e64fd-f30b-4765-81a0-62ad96dd167a``.
        To specify a web ACL created using AWS WAF Classic, use the ACL ID, for example ``473e64fd-f30b-4765-81a0-62ad96dd167a``.

        :default: - No AWS Web Application Firewall web access control list (web ACL).

        :see: https://docs.aws.amazon.com/cloudfront/latest/APIReference/API_CreateDistribution.html#API_CreateDistribution_RequestParameters.
        :stability: experimental
        '''
        result = self._values.get("web_acl_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DistributionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EdgeAstroSite(
    AstroSiteConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@astrojs-aws/construct.EdgeAstroSite",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        server_entry: builtins.str,
        static_dir: builtins.str,
        bucket_options: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        distribution_default_behavior_options: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        distribution_options: typing.Optional[typing.Union[DistributionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        server_options: typing.Optional[typing.Union["ServerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param server_entry: (experimental) The server entry file, e.g. path.join(__dirname, "../server/entry.mjs").
        :param static_dir: (experimental) The directory of static files, e.g. path.join(__dirname, "../dist/client").
        :param bucket_options: (experimental) Bucket options which is based on BucketProps. removalPolicy: @default RemovalPolicy.DESTROY autoDeleteObjects @default true,
        :param distribution_default_behavior_options: (experimental) CloudFront distribution default behavior options.
        :param distribution_options: (experimental) CloudFront distribution options.
        :param server_options: (experimental) The server options.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fbe348a9195063f1a9453096407ebb858ce229e12226bc0c46d7c853af18df9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EdgeAstroSiteProps(
            server_entry=server_entry,
            static_dir=static_dir,
            bucket_options=bucket_options,
            distribution_default_behavior_options=distribution_default_behavior_options,
            distribution_options=distribution_options,
            server_options=server_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="edgeFunction")
    def edge_function(self) -> _aws_cdk_aws_lambda_nodejs_ceddda9d.NodejsFunction:
        '''(experimental) Return edge function.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_lambda_nodejs_ceddda9d.NodejsFunction, jsii.invoke(self, "edgeFunction", []))

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @builtins.property
    @jsii.member(jsii_name="distributionDomainName")
    def distribution_domain_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "distributionDomainName"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))


@jsii.data_type(
    jsii_type="@astrojs-aws/construct.EdgeAstroSiteProps",
    jsii_struct_bases=[],
    name_mapping={
        "server_entry": "serverEntry",
        "static_dir": "staticDir",
        "bucket_options": "bucketOptions",
        "distribution_default_behavior_options": "distributionDefaultBehaviorOptions",
        "distribution_options": "distributionOptions",
        "server_options": "serverOptions",
    },
)
class EdgeAstroSiteProps:
    def __init__(
        self,
        *,
        server_entry: builtins.str,
        static_dir: builtins.str,
        bucket_options: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        distribution_default_behavior_options: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        distribution_options: typing.Optional[typing.Union[DistributionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        server_options: typing.Optional[typing.Union["ServerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) The options for the EdgeAstroSite.

        :param server_entry: (experimental) The server entry file, e.g. path.join(__dirname, "../server/entry.mjs").
        :param static_dir: (experimental) The directory of static files, e.g. path.join(__dirname, "../dist/client").
        :param bucket_options: (experimental) Bucket options which is based on BucketProps. removalPolicy: @default RemovalPolicy.DESTROY autoDeleteObjects @default true,
        :param distribution_default_behavior_options: (experimental) CloudFront distribution default behavior options.
        :param distribution_options: (experimental) CloudFront distribution options.
        :param server_options: (experimental) The server options.

        :stability: experimental
        '''
        if isinstance(bucket_options, dict):
            bucket_options = _aws_cdk_aws_s3_ceddda9d.BucketProps(**bucket_options)
        if isinstance(distribution_default_behavior_options, dict):
            distribution_default_behavior_options = _aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions(**distribution_default_behavior_options)
        if isinstance(distribution_options, dict):
            distribution_options = DistributionOptions(**distribution_options)
        if isinstance(server_options, dict):
            server_options = ServerOptions(**server_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8305299a6901c6df438fea789539465c466d30dc2750bc7f5ce3caa6c5fd264)
            check_type(argname="argument server_entry", value=server_entry, expected_type=type_hints["server_entry"])
            check_type(argname="argument static_dir", value=static_dir, expected_type=type_hints["static_dir"])
            check_type(argname="argument bucket_options", value=bucket_options, expected_type=type_hints["bucket_options"])
            check_type(argname="argument distribution_default_behavior_options", value=distribution_default_behavior_options, expected_type=type_hints["distribution_default_behavior_options"])
            check_type(argname="argument distribution_options", value=distribution_options, expected_type=type_hints["distribution_options"])
            check_type(argname="argument server_options", value=server_options, expected_type=type_hints["server_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "server_entry": server_entry,
            "static_dir": static_dir,
        }
        if bucket_options is not None:
            self._values["bucket_options"] = bucket_options
        if distribution_default_behavior_options is not None:
            self._values["distribution_default_behavior_options"] = distribution_default_behavior_options
        if distribution_options is not None:
            self._values["distribution_options"] = distribution_options
        if server_options is not None:
            self._values["server_options"] = server_options

    @builtins.property
    def server_entry(self) -> builtins.str:
        '''(experimental) The server entry file, e.g. path.join(__dirname, "../server/entry.mjs").

        :stability: experimental
        '''
        result = self._values.get("server_entry")
        assert result is not None, "Required property 'server_entry' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def static_dir(self) -> builtins.str:
        '''(experimental) The directory of static files, e.g. path.join(__dirname, "../dist/client").

        :stability: experimental
        '''
        result = self._values.get("static_dir")
        assert result is not None, "Required property 'static_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_options(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketProps]:
        '''(experimental) Bucket options which is based on BucketProps.

        removalPolicy: @default RemovalPolicy.DESTROY
        autoDeleteObjects @default true,

        :stability: experimental
        '''
        result = self._values.get("bucket_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketProps], result)

    @builtins.property
    def distribution_default_behavior_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions]:
        '''(experimental) CloudFront distribution default behavior options.

        :stability: experimental
        '''
        result = self._values.get("distribution_default_behavior_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions], result)

    @builtins.property
    def distribution_options(self) -> typing.Optional[DistributionOptions]:
        '''(experimental) CloudFront distribution options.

        :stability: experimental
        '''
        result = self._values.get("distribution_options")
        return typing.cast(typing.Optional[DistributionOptions], result)

    @builtins.property
    def server_options(self) -> typing.Optional["ServerOptions"]:
        '''(experimental) The server options.

        :stability: experimental
        '''
        result = self._values.get("server_options")
        return typing.cast(typing.Optional["ServerOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgeAstroSiteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaAstroSite(
    AstroSiteConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@astrojs-aws/construct.LambdaAstroSite",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        server_entry: builtins.str,
        static_dir: builtins.str,
        bucket_options: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        distribution_default_behavior_options: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        distribution_options: typing.Optional[typing.Union[DistributionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        http_api_options: typing.Optional[typing.Union[_aws_cdk_aws_apigatewayv2_alpha_050969fe.HttpApiProps, typing.Dict[builtins.str, typing.Any]]] = None,
        server_options: typing.Optional[typing.Union["ServerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param server_entry: (experimental) The server entry file, e.g. path.join(__dirname, "../server/entry.mjs").
        :param static_dir: (experimental) The directory of static files, e.g. path.join(__dirname, "../dist/client").
        :param bucket_options: (experimental) Bucket options which is based on BucketProps. removalPolicy: @default RemovalPolicy.DESTROY autoDeleteObjects @default true,
        :param distribution_default_behavior_options: (experimental) CloudFront distribution default behavior options.
        :param distribution_options: (experimental) CloudFront distribution options.
        :param http_api_options: (experimental) The HTTP api options.
        :param server_options: (experimental) The server options.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__919d2f7c50a313b0018ea18c98ec6f7aab019e1ede4395a72ac4ffe9cdb385b5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LambdaAstroSiteProps(
            server_entry=server_entry,
            static_dir=static_dir,
            bucket_options=bucket_options,
            distribution_default_behavior_options=distribution_default_behavior_options,
            distribution_options=distribution_options,
            http_api_options=http_api_options,
            server_options=server_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="api")
    def api(self) -> _aws_cdk_aws_apigatewayv2_alpha_050969fe.HttpApi:
        '''(experimental) return http api.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_apigatewayv2_alpha_050969fe.HttpApi, jsii.invoke(self, "api", []))

    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> _aws_cdk_aws_lambda_nodejs_ceddda9d.NodejsFunction:
        '''(experimental) Returns lambda function.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_lambda_nodejs_ceddda9d.NodejsFunction, jsii.invoke(self, "lambdaFunction", []))

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @builtins.property
    @jsii.member(jsii_name="distributionDomainName")
    def distribution_domain_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "distributionDomainName"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))


@jsii.data_type(
    jsii_type="@astrojs-aws/construct.LambdaAstroSiteProps",
    jsii_struct_bases=[],
    name_mapping={
        "server_entry": "serverEntry",
        "static_dir": "staticDir",
        "bucket_options": "bucketOptions",
        "distribution_default_behavior_options": "distributionDefaultBehaviorOptions",
        "distribution_options": "distributionOptions",
        "http_api_options": "httpApiOptions",
        "server_options": "serverOptions",
    },
)
class LambdaAstroSiteProps:
    def __init__(
        self,
        *,
        server_entry: builtins.str,
        static_dir: builtins.str,
        bucket_options: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        distribution_default_behavior_options: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        distribution_options: typing.Optional[typing.Union[DistributionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        http_api_options: typing.Optional[typing.Union[_aws_cdk_aws_apigatewayv2_alpha_050969fe.HttpApiProps, typing.Dict[builtins.str, typing.Any]]] = None,
        server_options: typing.Optional[typing.Union["ServerOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) The options for the LambdaAstroSite.

        :param server_entry: (experimental) The server entry file, e.g. path.join(__dirname, "../server/entry.mjs").
        :param static_dir: (experimental) The directory of static files, e.g. path.join(__dirname, "../dist/client").
        :param bucket_options: (experimental) Bucket options which is based on BucketProps. removalPolicy: @default RemovalPolicy.DESTROY autoDeleteObjects @default true,
        :param distribution_default_behavior_options: (experimental) CloudFront distribution default behavior options.
        :param distribution_options: (experimental) CloudFront distribution options.
        :param http_api_options: (experimental) The HTTP api options.
        :param server_options: (experimental) The server options.

        :stability: experimental
        '''
        if isinstance(bucket_options, dict):
            bucket_options = _aws_cdk_aws_s3_ceddda9d.BucketProps(**bucket_options)
        if isinstance(distribution_default_behavior_options, dict):
            distribution_default_behavior_options = _aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions(**distribution_default_behavior_options)
        if isinstance(distribution_options, dict):
            distribution_options = DistributionOptions(**distribution_options)
        if isinstance(http_api_options, dict):
            http_api_options = _aws_cdk_aws_apigatewayv2_alpha_050969fe.HttpApiProps(**http_api_options)
        if isinstance(server_options, dict):
            server_options = ServerOptions(**server_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3efb3975e83a8896ea9851eccf4181ddb1252978a00a5d4e0125d4525ea8fd4)
            check_type(argname="argument server_entry", value=server_entry, expected_type=type_hints["server_entry"])
            check_type(argname="argument static_dir", value=static_dir, expected_type=type_hints["static_dir"])
            check_type(argname="argument bucket_options", value=bucket_options, expected_type=type_hints["bucket_options"])
            check_type(argname="argument distribution_default_behavior_options", value=distribution_default_behavior_options, expected_type=type_hints["distribution_default_behavior_options"])
            check_type(argname="argument distribution_options", value=distribution_options, expected_type=type_hints["distribution_options"])
            check_type(argname="argument http_api_options", value=http_api_options, expected_type=type_hints["http_api_options"])
            check_type(argname="argument server_options", value=server_options, expected_type=type_hints["server_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "server_entry": server_entry,
            "static_dir": static_dir,
        }
        if bucket_options is not None:
            self._values["bucket_options"] = bucket_options
        if distribution_default_behavior_options is not None:
            self._values["distribution_default_behavior_options"] = distribution_default_behavior_options
        if distribution_options is not None:
            self._values["distribution_options"] = distribution_options
        if http_api_options is not None:
            self._values["http_api_options"] = http_api_options
        if server_options is not None:
            self._values["server_options"] = server_options

    @builtins.property
    def server_entry(self) -> builtins.str:
        '''(experimental) The server entry file, e.g. path.join(__dirname, "../server/entry.mjs").

        :stability: experimental
        '''
        result = self._values.get("server_entry")
        assert result is not None, "Required property 'server_entry' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def static_dir(self) -> builtins.str:
        '''(experimental) The directory of static files, e.g. path.join(__dirname, "../dist/client").

        :stability: experimental
        '''
        result = self._values.get("static_dir")
        assert result is not None, "Required property 'static_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_options(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketProps]:
        '''(experimental) Bucket options which is based on BucketProps.

        removalPolicy: @default RemovalPolicy.DESTROY
        autoDeleteObjects @default true,

        :stability: experimental
        '''
        result = self._values.get("bucket_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketProps], result)

    @builtins.property
    def distribution_default_behavior_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions]:
        '''(experimental) CloudFront distribution default behavior options.

        :stability: experimental
        '''
        result = self._values.get("distribution_default_behavior_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions], result)

    @builtins.property
    def distribution_options(self) -> typing.Optional[DistributionOptions]:
        '''(experimental) CloudFront distribution options.

        :stability: experimental
        '''
        result = self._values.get("distribution_options")
        return typing.cast(typing.Optional[DistributionOptions], result)

    @builtins.property
    def http_api_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.HttpApiProps]:
        '''(experimental) The HTTP api options.

        :stability: experimental
        '''
        result = self._values.get("http_api_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_alpha_050969fe.HttpApiProps], result)

    @builtins.property
    def server_options(self) -> typing.Optional["ServerOptions"]:
        '''(experimental) The server options.

        :stability: experimental
        '''
        result = self._values.get("server_options")
        return typing.cast(typing.Optional["ServerOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaAstroSiteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@astrojs-aws/construct.ServerOptions",
    jsii_struct_bases=[_aws_cdk_aws_lambda_ceddda9d.FunctionOptions],
    name_mapping={
        "max_event_age": "maxEventAge",
        "on_failure": "onFailure",
        "on_success": "onSuccess",
        "retry_attempts": "retryAttempts",
        "adot_instrumentation": "adotInstrumentation",
        "allow_all_outbound": "allowAllOutbound",
        "allow_public_subnet": "allowPublicSubnet",
        "architecture": "architecture",
        "code_signing_config": "codeSigningConfig",
        "current_version_options": "currentVersionOptions",
        "dead_letter_queue": "deadLetterQueue",
        "dead_letter_queue_enabled": "deadLetterQueueEnabled",
        "dead_letter_topic": "deadLetterTopic",
        "description": "description",
        "environment": "environment",
        "environment_encryption": "environmentEncryption",
        "ephemeral_storage_size": "ephemeralStorageSize",
        "events": "events",
        "filesystem": "filesystem",
        "function_name": "functionName",
        "initial_policy": "initialPolicy",
        "insights_version": "insightsVersion",
        "layers": "layers",
        "log_retention": "logRetention",
        "log_retention_retry_options": "logRetentionRetryOptions",
        "log_retention_role": "logRetentionRole",
        "memory_size": "memorySize",
        "profiling": "profiling",
        "profiling_group": "profilingGroup",
        "reserved_concurrent_executions": "reservedConcurrentExecutions",
        "role": "role",
        "runtime_management_mode": "runtimeManagementMode",
        "security_groups": "securityGroups",
        "timeout": "timeout",
        "tracing": "tracing",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "bundling": "bundling",
        "runtime": "runtime",
    },
)
class ServerOptions(_aws_cdk_aws_lambda_ceddda9d.FunctionOptions):
    def __init__(
        self,
        *,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        on_failure: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        on_success: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        adot_instrumentation: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
        code_signing_config: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig] = None,
        current_version_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.VersionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
        dead_letter_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        events: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.IEventSource]] = None,
        filesystem: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem] = None,
        function_name: typing.Optional[builtins.str] = None,
        initial_policy: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
        insights_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion] = None,
        layers: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        profiling: typing.Optional[builtins.bool] = None,
        profiling_group: typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        runtime_management_mode: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        tracing: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        bundling: typing.Optional[typing.Union[_aws_cdk_aws_lambda_nodejs_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        runtime: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The options for the lambda function.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param adot_instrumentation: Specify the configuration of AWS Distro for OpenTelemetry (ADOT) instrumentation. Default: - No ADOT instrumentation
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param allow_public_subnet: Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param architecture: The system architectures compatible with this lambda function. Default: Architecture.X86_64
        :param code_signing_config: Code signing config associated with this function. Default: - Not Sign the Code
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. If SNS topic is desired, specify ``deadLetterTopic`` property instead. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param dead_letter_topic: The SNS topic to use as a DLQ. Note that if ``deadLetterQueueEnabled`` is set to ``true``, an SQS queue will be created rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly. Default: - no SNS topic
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param environment_encryption: The AWS KMS key that's used to encrypt your function's environment variables. Default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        :param ephemeral_storage_size: The size of the function’s /tmp directory in MiB. Default: 512 MiB
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param insights_version: Specify the version of CloudWatch Lambda insights to use for monitoring. Default: - No Lambda Insights
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by multiple functions. Default: - No layers.
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param profiling: Enable profiling. Default: - No profiling.
        :param profiling_group: Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param runtime_management_mode: Sets the runtime management configuration for a function's version. Default: Auto
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. This is required when ``vpcSubnets`` is specified. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. This requires ``vpc`` to be specified in order for interfaces to actually be placed in the subnets. If ``vpc`` is not specify, this will raise an error. Note: Internet access for Lambda Functions requires a NAT Gateway, so picking public subnets is not allowed (unless ``allowPublicSubnet`` is set to ``true``). Default: - the Vpc default strategy if not specified
        :param bundling: (experimental) Bundling options.
        :param runtime: (experimental) The Nodejs Runtime. Default: nodejs18.x

        :stability: experimental
        '''
        if isinstance(adot_instrumentation, dict):
            adot_instrumentation = _aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig(**adot_instrumentation)
        if isinstance(current_version_options, dict):
            current_version_options = _aws_cdk_aws_lambda_ceddda9d.VersionOptions(**current_version_options)
        if isinstance(log_retention_retry_options, dict):
            log_retention_retry_options = _aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions(**log_retention_retry_options)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if isinstance(bundling, dict):
            bundling = _aws_cdk_aws_lambda_nodejs_ceddda9d.BundlingOptions(**bundling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37953f1eba9b563d1341cf75bd7d73a57ac96383b9d4bbcb3ad5ab140341b32e)
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            check_type(argname="argument on_success", value=on_success, expected_type=type_hints["on_success"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument adot_instrumentation", value=adot_instrumentation, expected_type=type_hints["adot_instrumentation"])
            check_type(argname="argument allow_all_outbound", value=allow_all_outbound, expected_type=type_hints["allow_all_outbound"])
            check_type(argname="argument allow_public_subnet", value=allow_public_subnet, expected_type=type_hints["allow_public_subnet"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument code_signing_config", value=code_signing_config, expected_type=type_hints["code_signing_config"])
            check_type(argname="argument current_version_options", value=current_version_options, expected_type=type_hints["current_version_options"])
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument dead_letter_queue_enabled", value=dead_letter_queue_enabled, expected_type=type_hints["dead_letter_queue_enabled"])
            check_type(argname="argument dead_letter_topic", value=dead_letter_topic, expected_type=type_hints["dead_letter_topic"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument environment_encryption", value=environment_encryption, expected_type=type_hints["environment_encryption"])
            check_type(argname="argument ephemeral_storage_size", value=ephemeral_storage_size, expected_type=type_hints["ephemeral_storage_size"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument filesystem", value=filesystem, expected_type=type_hints["filesystem"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument initial_policy", value=initial_policy, expected_type=type_hints["initial_policy"])
            check_type(argname="argument insights_version", value=insights_version, expected_type=type_hints["insights_version"])
            check_type(argname="argument layers", value=layers, expected_type=type_hints["layers"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument log_retention_retry_options", value=log_retention_retry_options, expected_type=type_hints["log_retention_retry_options"])
            check_type(argname="argument log_retention_role", value=log_retention_role, expected_type=type_hints["log_retention_role"])
            check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
            check_type(argname="argument profiling", value=profiling, expected_type=type_hints["profiling"])
            check_type(argname="argument profiling_group", value=profiling_group, expected_type=type_hints["profiling_group"])
            check_type(argname="argument reserved_concurrent_executions", value=reserved_concurrent_executions, expected_type=type_hints["reserved_concurrent_executions"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument runtime_management_mode", value=runtime_management_mode, expected_type=type_hints["runtime_management_mode"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument tracing", value=tracing, expected_type=type_hints["tracing"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument bundling", value=bundling, expected_type=type_hints["bundling"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if on_success is not None:
            self._values["on_success"] = on_success
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if adot_instrumentation is not None:
            self._values["adot_instrumentation"] = adot_instrumentation
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if allow_public_subnet is not None:
            self._values["allow_public_subnet"] = allow_public_subnet
        if architecture is not None:
            self._values["architecture"] = architecture
        if code_signing_config is not None:
            self._values["code_signing_config"] = code_signing_config
        if current_version_options is not None:
            self._values["current_version_options"] = current_version_options
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if dead_letter_queue_enabled is not None:
            self._values["dead_letter_queue_enabled"] = dead_letter_queue_enabled
        if dead_letter_topic is not None:
            self._values["dead_letter_topic"] = dead_letter_topic
        if description is not None:
            self._values["description"] = description
        if environment is not None:
            self._values["environment"] = environment
        if environment_encryption is not None:
            self._values["environment_encryption"] = environment_encryption
        if ephemeral_storage_size is not None:
            self._values["ephemeral_storage_size"] = ephemeral_storage_size
        if events is not None:
            self._values["events"] = events
        if filesystem is not None:
            self._values["filesystem"] = filesystem
        if function_name is not None:
            self._values["function_name"] = function_name
        if initial_policy is not None:
            self._values["initial_policy"] = initial_policy
        if insights_version is not None:
            self._values["insights_version"] = insights_version
        if layers is not None:
            self._values["layers"] = layers
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if log_retention_retry_options is not None:
            self._values["log_retention_retry_options"] = log_retention_retry_options
        if log_retention_role is not None:
            self._values["log_retention_role"] = log_retention_role
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if profiling is not None:
            self._values["profiling"] = profiling
        if profiling_group is not None:
            self._values["profiling_group"] = profiling_group
        if reserved_concurrent_executions is not None:
            self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None:
            self._values["role"] = role
        if runtime_management_mode is not None:
            self._values["runtime_management_mode"] = runtime_management_mode
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if timeout is not None:
            self._values["timeout"] = timeout
        if tracing is not None:
            self._values["tracing"] = tracing
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if bundling is not None:
            self._values["bundling"] = bundling
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def max_event_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        :default: Duration.hours(6)
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def on_failure(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination]:
        '''The destination for failed invocations.

        :default: - no destination
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination], result)

    @builtins.property
    def on_success(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination]:
        '''The destination for successful invocations.

        :default: - no destination
        '''
        result = self._values.get("on_success")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        :default: 2
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def adot_instrumentation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig]:
        '''Specify the configuration of AWS Distro for OpenTelemetry (ADOT) instrumentation.

        :default: - No ADOT instrumentation

        :see: https://aws-otel.github.io/docs/getting-started/lambda
        '''
        result = self._values.get("adot_instrumentation")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig], result)

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        '''Whether to allow the Lambda to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        Lambda to connect to network targets.

        :default: true
        '''
        result = self._values.get("allow_all_outbound")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_public_subnet(self) -> typing.Optional[builtins.bool]:
        '''Lambda Functions in a public subnet can NOT access the internet.

        Use this property to acknowledge this limitation and still place the function in a public subnet.

        :default: false

        :see: https://stackoverflow.com/questions/52992085/why-cant-an-aws-lambda-function-inside-a-public-subnet-in-a-vpc-connect-to-the/52994841#52994841
        '''
        result = self._values.get("allow_public_subnet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def architecture(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture]:
        '''The system architectures compatible with this lambda function.

        :default: Architecture.X86_64
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture], result)

    @builtins.property
    def code_signing_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig]:
        '''Code signing config associated with this function.

        :default: - Not Sign the Code
        '''
        result = self._values.get("code_signing_config")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig], result)

    @builtins.property
    def current_version_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.VersionOptions]:
        '''Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method.

        :default: - default options as described in ``VersionOptions``
        '''
        result = self._values.get("current_version_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.VersionOptions], result)

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''The SQS queue to use if DLQ is enabled.

        If SNS topic is desired, specify ``deadLetterTopic`` property instead.

        :default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def dead_letter_queue_enabled(self) -> typing.Optional[builtins.bool]:
        '''Enabled DLQ.

        If ``deadLetterQueue`` is undefined,
        an SQS queue with default options will be defined for your Function.

        :default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        '''
        result = self._values.get("dead_letter_queue_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dead_letter_topic(self) -> typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic]:
        '''The SNS topic to use as a DLQ.

        Note that if ``deadLetterQueueEnabled`` is set to ``true``, an SQS queue will be created
        rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly.

        :default: - no SNS topic
        '''
        result = self._values.get("dead_letter_topic")
        return typing.cast(typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the function.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Key-value pairs that Lambda caches and makes available for your Lambda functions.

        Use environment variables to apply configuration changes, such
        as test and production environment configurations, without changing your
        Lambda function source code.

        :default: - No environment variables.
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment_encryption(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The AWS KMS key that's used to encrypt your function's environment variables.

        :default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        '''
        result = self._values.get("environment_encryption")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def ephemeral_storage_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''The size of the function’s /tmp directory in MiB.

        :default: 512 MiB
        '''
        result = self._values.get("ephemeral_storage_size")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def events(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_lambda_ceddda9d.IEventSource]]:
        '''Event sources for this function.

        You can also add event sources using ``addEventSource``.

        :default: - No event sources.
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_lambda_ceddda9d.IEventSource]], result)

    @builtins.property
    def filesystem(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem]:
        '''The filesystem configuration for the lambda function.

        :default: - will not mount any filesystem
        '''
        result = self._values.get("filesystem")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''A name for the function.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that
        ID for the function's name. For more information, see Name Type.
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_policy(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]]:
        '''Initial policy statements to add to the created Lambda Role.

        You can call ``addToRolePolicy`` to the created lambda to add statements post creation.

        :default: - No policy statements are added to the created Lambda role.
        '''
        result = self._values.get("initial_policy")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]], result)

    @builtins.property
    def insights_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion]:
        '''Specify the version of CloudWatch Lambda insights to use for monitoring.

        :default: - No Lambda Insights

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights-Getting-Started-docker.html
        '''
        result = self._values.get("insights_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion], result)

    @builtins.property
    def layers(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]]:
        '''A list of layers to add to the function's execution environment.

        You can configure your Lambda function to pull in
        additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies
        that can be used by multiple functions.

        :default: - No layers.
        '''
        result = self._values.get("layers")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.INFINITE
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def log_retention_retry_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions]:
        '''When log retention is specified, a custom resource attempts to create the CloudWatch log group.

        These options control the retry policy when interacting with CloudWatch APIs.

        :default: - Default AWS SDK retry options.
        '''
        result = self._values.get("log_retention_retry_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions], result)

    @builtins.property
    def log_retention_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        :default: - A new role is created.
        '''
        result = self._values.get("log_retention_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''The amount of memory, in MB, that is allocated to your Lambda function.

        Lambda uses this value to proportionally allocate the amount of CPU
        power. For more information, see Resource Model in the AWS Lambda
        Developer Guide.

        :default: 128
        '''
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def profiling(self) -> typing.Optional[builtins.bool]:
        '''Enable profiling.

        :default: - No profiling.

        :see: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html
        '''
        result = self._values.get("profiling")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def profiling_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup]:
        '''Profiling Group.

        :default: - A new profiling group will be created if ``profiling`` is set.

        :see: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html
        '''
        result = self._values.get("profiling_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup], result)

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        '''The maximum of concurrent executions you want to reserve for the function.

        :default: - No specific limit - account limit.

        :see: https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html
        '''
        result = self._values.get("reserved_concurrent_executions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''Lambda execution role.

        This is the role that will be assumed by the function upon execution.
        It controls the permissions that the function will have. The Role must
        be assumable by the 'lambda.amazonaws.com' service principal.

        The default Role automatically has permissions granted for Lambda execution. If you
        provide a Role, you must add the relevant AWS managed policies yourself.

        The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and
        "service-role/AWSLambdaVPCAccessExecutionRole".

        :default:

        - A unique role will be generated for this lambda function.
        Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def runtime_management_mode(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode]:
        '''Sets the runtime management configuration for a function's version.

        :default: Auto
        '''
        result = self._values.get("runtime_management_mode")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''The list of security groups to associate with the Lambda's network interfaces.

        Only used if 'vpc' is supplied.

        :default:

        - If the function is placed within a VPC and a security group is
        not specified, either by this or securityGroup prop, a dedicated security
        group will be created for this function.
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The function execution time (in seconds) after which Lambda terminates the function.

        Because the execution time affects cost, set this value
        based on the function's expected execution time.

        :default: Duration.seconds(3)
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def tracing(self) -> typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing]:
        '''Enable AWS X-Ray Tracing for Lambda Function.

        :default: Tracing.Disabled
        '''
        result = self._values.get("tracing")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''VPC network to place Lambda network interfaces.

        Specify this if the Lambda function needs to access resources in a VPC.
        This is required when ``vpcSubnets`` is specified.

        :default: - Function is not placed within a VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Where to place the network interfaces within the VPC.

        This requires ``vpc`` to be specified in order for interfaces to actually be
        placed in the subnets. If ``vpc`` is not specify, this will raise an error.

        Note: Internet access for Lambda Functions requires a NAT Gateway, so picking
        public subnets is not allowed (unless ``allowPublicSubnet`` is set to ``true``).

        :default: - the Vpc default strategy if not specified
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def bundling(
        self,
    ) -> typing.Optional[_aws_cdk_aws_lambda_nodejs_ceddda9d.BundlingOptions]:
        '''(experimental) Bundling options.

        :stability: experimental
        '''
        result = self._values.get("bundling")
        return typing.cast(typing.Optional[_aws_cdk_aws_lambda_nodejs_ceddda9d.BundlingOptions], result)

    @builtins.property
    def runtime(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Nodejs Runtime.

        :default: nodejs18.x

        :stability: experimental
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StaticAstroSite(
    AstroSiteConstruct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@astrojs-aws/construct.StaticAstroSite",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        static_dir: builtins.str,
        bucket_options: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        distribution_default_behavior_options: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        distribution_options: typing.Optional[typing.Union[DistributionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param static_dir: (experimental) The directory of built files, e.g. path.join(__dirname, "../dist").
        :param bucket_options: (experimental) Bucket options which is based on BucketProps. removalPolicy: @default RemovalPolicy.DESTROY autoDeleteObjects @default true,
        :param distribution_default_behavior_options: (experimental) CloudFront distribution default behavior options.
        :param distribution_options: (experimental) CloudFront distribution options.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7c1078f47a089ec32759a5895dbdd9baee0042d6d1f2f5014d04a76b084ca0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StaticAstroSiteProps(
            static_dir=static_dir,
            bucket_options=bucket_options,
            distribution_default_behavior_options=distribution_default_behavior_options,
            distribution_options=distribution_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @builtins.property
    @jsii.member(jsii_name="bucketName")
    def bucket_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "bucketName"))

    @builtins.property
    @jsii.member(jsii_name="distributionDomainName")
    def distribution_domain_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "distributionDomainName"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))


@jsii.data_type(
    jsii_type="@astrojs-aws/construct.StaticAstroSiteProps",
    jsii_struct_bases=[],
    name_mapping={
        "static_dir": "staticDir",
        "bucket_options": "bucketOptions",
        "distribution_default_behavior_options": "distributionDefaultBehaviorOptions",
        "distribution_options": "distributionOptions",
    },
)
class StaticAstroSiteProps:
    def __init__(
        self,
        *,
        static_dir: builtins.str,
        bucket_options: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
        distribution_default_behavior_options: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        distribution_options: typing.Optional[typing.Union[DistributionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) The options for the StaticAstroSite.

        :param static_dir: (experimental) The directory of built files, e.g. path.join(__dirname, "../dist").
        :param bucket_options: (experimental) Bucket options which is based on BucketProps. removalPolicy: @default RemovalPolicy.DESTROY autoDeleteObjects @default true,
        :param distribution_default_behavior_options: (experimental) CloudFront distribution default behavior options.
        :param distribution_options: (experimental) CloudFront distribution options.

        :stability: experimental
        '''
        if isinstance(bucket_options, dict):
            bucket_options = _aws_cdk_aws_s3_ceddda9d.BucketProps(**bucket_options)
        if isinstance(distribution_default_behavior_options, dict):
            distribution_default_behavior_options = _aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions(**distribution_default_behavior_options)
        if isinstance(distribution_options, dict):
            distribution_options = DistributionOptions(**distribution_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3325321ebadc5e36cd8f3b8ad8b45edb7386a70e17bc2b7a0976fb7ae04ab39e)
            check_type(argname="argument static_dir", value=static_dir, expected_type=type_hints["static_dir"])
            check_type(argname="argument bucket_options", value=bucket_options, expected_type=type_hints["bucket_options"])
            check_type(argname="argument distribution_default_behavior_options", value=distribution_default_behavior_options, expected_type=type_hints["distribution_default_behavior_options"])
            check_type(argname="argument distribution_options", value=distribution_options, expected_type=type_hints["distribution_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "static_dir": static_dir,
        }
        if bucket_options is not None:
            self._values["bucket_options"] = bucket_options
        if distribution_default_behavior_options is not None:
            self._values["distribution_default_behavior_options"] = distribution_default_behavior_options
        if distribution_options is not None:
            self._values["distribution_options"] = distribution_options

    @builtins.property
    def static_dir(self) -> builtins.str:
        '''(experimental) The directory of built files, e.g. path.join(__dirname, "../dist").

        :stability: experimental
        '''
        result = self._values.get("static_dir")
        assert result is not None, "Required property 'static_dir' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bucket_options(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketProps]:
        '''(experimental) Bucket options which is based on BucketProps.

        removalPolicy: @default RemovalPolicy.DESTROY
        autoDeleteObjects @default true,

        :stability: experimental
        '''
        result = self._values.get("bucket_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketProps], result)

    @builtins.property
    def distribution_default_behavior_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions]:
        '''(experimental) CloudFront distribution default behavior options.

        :stability: experimental
        '''
        result = self._values.get("distribution_default_behavior_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions], result)

    @builtins.property
    def distribution_options(self) -> typing.Optional[DistributionOptions]:
        '''(experimental) CloudFront distribution options.

        :stability: experimental
        '''
        result = self._values.get("distribution_options")
        return typing.cast(typing.Optional[DistributionOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StaticAstroSiteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AstroSiteConstruct",
    "DistributionOptions",
    "EdgeAstroSite",
    "EdgeAstroSiteProps",
    "LambdaAstroSite",
    "LambdaAstroSiteProps",
    "ServerOptions",
    "StaticAstroSite",
    "StaticAstroSiteProps",
]

publication.publish()

def _typecheckingstub__db9d982b9095784bc59520b993f10dfaad2bbd6ee2cb8c80aa143a1c8c6d25a8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a04f0b61812d848db8d60a2935ebfc24eb9b442dc947ccedced2b672fafbcbb(
    scope: _constructs_77d1e7e8.Construct,
    static_dir: builtins.str,
    *,
    access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
    auto_delete_objects: typing.Optional[builtins.bool] = None,
    block_public_access: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BlockPublicAccess] = None,
    bucket_key_enabled: typing.Optional[builtins.bool] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    cors: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.CorsRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    encryption: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketEncryption] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    enforce_ssl: typing.Optional[builtins.bool] = None,
    event_bridge_enabled: typing.Optional[builtins.bool] = None,
    intelligent_tiering_configurations: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.IntelligentTieringConfiguration, typing.Dict[builtins.str, typing.Any]]]] = None,
    inventories: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.Inventory, typing.Dict[builtins.str, typing.Any]]]] = None,
    lifecycle_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.LifecycleRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    metrics: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketMetrics, typing.Dict[builtins.str, typing.Any]]]] = None,
    notifications_handler_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    object_lock_default_retention: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectLockRetention] = None,
    object_lock_enabled: typing.Optional[builtins.bool] = None,
    object_ownership: typing.Optional[_aws_cdk_aws_s3_ceddda9d.ObjectOwnership] = None,
    public_read_access: typing.Optional[builtins.bool] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    server_access_logs_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    server_access_logs_prefix: typing.Optional[builtins.str] = None,
    transfer_acceleration: typing.Optional[builtins.bool] = None,
    versioned: typing.Optional[builtins.bool] = None,
    website_error_document: typing.Optional[builtins.str] = None,
    website_index_document: typing.Optional[builtins.str] = None,
    website_redirect: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.RedirectTarget, typing.Dict[builtins.str, typing.Any]]] = None,
    website_routing_rules: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_s3_ceddda9d.RoutingRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ed10c38699730e2bf5e69ee0bd4925e438d4799a5852709f308f2affea6d7f(
    scope: _constructs_77d1e7e8.Construct,
    server_entry: builtins.str,
    *,
    bundling: typing.Optional[typing.Union[_aws_cdk_aws_lambda_nodejs_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime: typing.Optional[builtins.str] = None,
    adot_instrumentation: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    allow_public_subnet: typing.Optional[builtins.bool] = None,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    code_signing_config: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig] = None,
    current_version_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.VersionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
    dead_letter_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    description: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment_encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    events: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.IEventSource]] = None,
    filesystem: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem] = None,
    function_name: typing.Optional[builtins.str] = None,
    initial_policy: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    insights_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion] = None,
    layers: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    profiling: typing.Optional[builtins.bool] = None,
    profiling_group: typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    runtime_management_mode: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    tracing: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    on_failure: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    on_success: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b421adfa617ab976e8d23db7cc054c672a89b03727bc8aea382f4f4d5f4fef2e(
    scope: _constructs_77d1e7e8.Construct,
    bucket: _aws_cdk_aws_s3_ceddda9d.Bucket,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf3fb2a8029aa3b0236943223b8d34ab2cc4770d3bfaa828c426b76ea51d6cd(
    dir: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce4b161f41068601e658dcd2dbe5f267f30e7aa75918596cd3c3a81973920c1(
    str: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74a8a4e0de802e6bca8967c29913a63486c9eb1716556f1cb7e8757dc87a7ed(
    *,
    additional_behaviors: typing.Optional[typing.Mapping[builtins.str, typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.BehaviorOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
    comment: typing.Optional[builtins.str] = None,
    domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[builtins.bool] = None,
    enable_ipv6: typing.Optional[builtins.bool] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    error_responses: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse, typing.Dict[builtins.str, typing.Any]]]] = None,
    geo_restriction: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction] = None,
    http_version: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion] = None,
    log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    log_file_prefix: typing.Optional[builtins.str] = None,
    log_includes_cookies: typing.Optional[builtins.bool] = None,
    minimum_protocol_version: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SecurityPolicyProtocol] = None,
    price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
    ssl_support_method: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.SSLMethod] = None,
    web_acl_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fbe348a9195063f1a9453096407ebb858ce229e12226bc0c46d7c853af18df9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    server_entry: builtins.str,
    static_dir: builtins.str,
    bucket_options: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
    distribution_default_behavior_options: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    distribution_options: typing.Optional[typing.Union[DistributionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    server_options: typing.Optional[typing.Union[ServerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8305299a6901c6df438fea789539465c466d30dc2750bc7f5ce3caa6c5fd264(
    *,
    server_entry: builtins.str,
    static_dir: builtins.str,
    bucket_options: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
    distribution_default_behavior_options: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    distribution_options: typing.Optional[typing.Union[DistributionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    server_options: typing.Optional[typing.Union[ServerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__919d2f7c50a313b0018ea18c98ec6f7aab019e1ede4395a72ac4ffe9cdb385b5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    server_entry: builtins.str,
    static_dir: builtins.str,
    bucket_options: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
    distribution_default_behavior_options: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    distribution_options: typing.Optional[typing.Union[DistributionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    http_api_options: typing.Optional[typing.Union[_aws_cdk_aws_apigatewayv2_alpha_050969fe.HttpApiProps, typing.Dict[builtins.str, typing.Any]]] = None,
    server_options: typing.Optional[typing.Union[ServerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3efb3975e83a8896ea9851eccf4181ddb1252978a00a5d4e0125d4525ea8fd4(
    *,
    server_entry: builtins.str,
    static_dir: builtins.str,
    bucket_options: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
    distribution_default_behavior_options: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    distribution_options: typing.Optional[typing.Union[DistributionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    http_api_options: typing.Optional[typing.Union[_aws_cdk_aws_apigatewayv2_alpha_050969fe.HttpApiProps, typing.Dict[builtins.str, typing.Any]]] = None,
    server_options: typing.Optional[typing.Union[ServerOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37953f1eba9b563d1341cf75bd7d73a57ac96383b9d4bbcb3ad5ab140341b32e(
    *,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    on_failure: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    on_success: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IDestination] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    adot_instrumentation: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.AdotInstrumentationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    allow_public_subnet: typing.Optional[builtins.bool] = None,
    architecture: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Architecture] = None,
    code_signing_config: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.ICodeSigningConfig] = None,
    current_version_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.VersionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
    dead_letter_topic: typing.Optional[_aws_cdk_aws_sns_ceddda9d.ITopic] = None,
    description: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment_encryption: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    events: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.IEventSource]] = None,
    filesystem: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.FileSystem] = None,
    function_name: typing.Optional[builtins.str] = None,
    initial_policy: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    insights_version: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.LambdaInsightsVersion] = None,
    layers: typing.Optional[typing.Sequence[_aws_cdk_aws_lambda_ceddda9d.ILayerVersion]] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    log_retention_retry_options: typing.Optional[typing.Union[_aws_cdk_aws_lambda_ceddda9d.LogRetentionRetryOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    log_retention_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    profiling: typing.Optional[builtins.bool] = None,
    profiling_group: typing.Optional[_aws_cdk_aws_codeguruprofiler_ceddda9d.IProfilingGroup] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    runtime_management_mode: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.RuntimeManagementMode] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    tracing: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.Tracing] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    bundling: typing.Optional[typing.Union[_aws_cdk_aws_lambda_nodejs_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7c1078f47a089ec32759a5895dbdd9baee0042d6d1f2f5014d04a76b084ca0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    static_dir: builtins.str,
    bucket_options: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
    distribution_default_behavior_options: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    distribution_options: typing.Optional[typing.Union[DistributionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3325321ebadc5e36cd8f3b8ad8b45edb7386a70e17bc2b7a0976fb7ae04ab39e(
    *,
    static_dir: builtins.str,
    bucket_options: typing.Optional[typing.Union[_aws_cdk_aws_s3_ceddda9d.BucketProps, typing.Dict[builtins.str, typing.Any]]] = None,
    distribution_default_behavior_options: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.AddBehaviorOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    distribution_options: typing.Optional[typing.Union[DistributionOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
