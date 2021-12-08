import unittest
# unit tests
import tests.testNotification as testNotification
import tests.testRegularOperationType as  testRegularOperationType
import tests.testRegularOperation as testRegularOperation
import tests.testsDepositBalance as testsDepositBalance
import tests.testsPaymentsBalance as testsPaymentsBalance
import tests.testBusinessEntity as testBusinessEntity

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(testNotification.suite())
    runner.run(testRegularOperationType.suite())
    runner.run(testRegularOperation.suite())
    runner.run(testsDepositBalance.suite())
    runner.run(testsPaymentsBalance.suite())
    runner.run(testBusinessEntity.suite())
