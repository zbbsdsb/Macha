package dev.macha.layer.protocol

/** action_result.status（01 §3.6）。 */
object ActionStatus {
    const val OK = "ok"
    const val REFUSED = "refused"
    const val FAILED = "failed"
    const val PENDING = "pending"
}

/** refused 的 reason（01 §3.6 表）：环境做不到/不允许，**正常结果**非错误。 */
object RefusalReason {
    const val NOT_SUPPORTED = "not_supported"
    const val PRECONDITION_FAILED = "precondition_failed"
    const val OUT_OF_RANGE = "out_of_range"
    const val NO_PERMISSION = "no_permission"
}

/** failed 的 reason（01 §3.6 表）：尝试了但没成功。 */
object FailureReason {
    const val TARGET_MISSING = "target_missing"
    const val BLOCKED = "blocked"
    const val INTERNAL = "internal"
}

/** error.code 最小集（01 §3.7）。 */
object ErrorCode {
    const val BAD_VERSION = "bad_version"
    const val UNKNOWN_TYPE = "unknown_type"
    const val SCHEMA_VIOLATION = "schema_violation"
    const val UNAUTHORIZED = "unauthorized"
    const val INTERNAL = "internal"
}