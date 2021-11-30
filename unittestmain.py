import unittest
# unit tests
import testNotification
import testRegularOperationType
import testRegularOperation
import testsDepositBalance
import testsPaymentsBalance


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(testNotification.suite())
    runner.run(testRegularOperationType.suite())
    runner.run(testRegularOperation.suite())
    runner.run(testsDepositBalance.suite())
    runner.run(testsPaymentsBalance.suite())

