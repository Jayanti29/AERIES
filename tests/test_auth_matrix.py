import unittest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app.core.rbac import Role, ROLE_PERMISSIONS, has_permission

class TestAuthMatrix(unittest.TestCase):
    def test_deny_by_default(self):
        # A random role or permission should strictly deny
        self.assertFalse(has_permission("Guest", "command:read"))
        self.assertFalse(has_permission(Role.PILOT, "craft:maintenance"))

    def test_planner_cannot_approve(self):
        # Spec rule: Planners cannot approve own plans
        self.assertTrue(has_permission(Role.OPERATIONS_PLANNER, "plans:create"))
        self.assertFalse(has_permission(Role.OPERATIONS_PLANNER, "decisions:approve"))

    def test_authority_cannot_create_plans(self):
        # Spec rule: Decision Authority approves plans, cannot create plans
        self.assertTrue(has_permission(Role.DECISION_AUTHORITY, "decisions:approve"))
        self.assertFalse(has_permission(Role.DECISION_AUTHORITY, "plans:create"))

    def test_pilot_own_data_only(self):
        # Pilot can only see own state
        self.assertTrue(has_permission(Role.PILOT, "state:read_own"))
        self.assertFalse(has_permission(Role.PILOT, "people:read"))
        self.assertFalse(has_permission(Role.PILOT, "craft:read"))

    def test_personnel_unmask_restricted(self):
        # Only Personnel Officer has people:unmask permission
        self.assertTrue(has_permission(Role.PERSONNEL_OFFICER, "people:unmask"))
        self.assertFalse(has_permission(Role.CRAFT_OFFICER, "people:unmask"))
        self.assertFalse(has_permission(Role.SUPPLY_OFFICER, "people:unmask"))

if __name__ == '__main__':
    unittest.main()
