"""A component to simulate lifting surfaces vehicle."""
from __future__ import annotations

import warnings

import numpy as np
from pybullet_utils import bullet_client


class LiftingSurfaces:
    """Handler for multiple lifting surfaces."""

    def __init__(self, lifting_surfaces: list[LiftingSurface]):
        """__init__.

        Args:
            lifting_surfaces (list[LiftingSurface]): lifting_surfaces
        """
        # assert all is lifting surfaces
        assert all(
            [isinstance(surface, LiftingSurface) for surface in lifting_surfaces]
        )

        # store some stuff
        self.p = lifting_surfaces[0].p
        self.uav_id = lifting_surfaces[0].uav_id
        self.surfaces: list[LiftingSurface] = lifting_surfaces
        self.surface_ids = np.array([s.surface_id for s in self.surfaces])

    def reset(self):
        """Resets all lifting surfaces."""
        [surface.reset() for surface in self.surfaces]

    def get_states(self) -> np.ndarray:
        """Gets the current state of the components.

        Returns:
            np.ndarray:
        """
        return np.array([surface.actuation for surface in self.surfaces])

    def physics_update(self, cmd: np.ndarray):
        """Converts actuation commands into forces on the lifting surfaces.

        Args:
            cmd (np.ndarray): the full command array, command mapping is handled through `command_id` and `command_sign` on each surface.
        """
        assert np.all(cmd >= -1.0) and np.all(
            cmd <= 1.0
        ), f"`{cmd=} has values out of bounds of -1.0 and 1.0.`"

        for surface in self.surfaces:
            actuation = (
                0.0
                if surface.command_id is None
                else float(cmd[surface.command_id] * surface.command_sign)
            )

            surface.physics_update(actuation)

    def state_update(self, rotation_matrix: np.ndarray):
        """Updates all local surface velocities of the lifting surface, place under `update_state`.

        Args:
            rotation_matrix (np.ndarray): rotation_matrix of the main body
        """
        # get all the states for all the surfaces
        surface_velocities = self.p.getLinkStates(
            self.uav_id, self.surface_ids, computeLinkVelocity=True
        )

        # get all the velocities
        surface_velocities = np.array([item[-2] for item in surface_velocities])

        # convert all to local velocities
        surface_velocities = np.matmul(rotation_matrix, surface_velocities.T).T

        # update the velocities of all surfaces
        for surface, velocity in zip(self.surfaces, surface_velocities):
            surface.state_update(velocity)


class LiftingSurface:
    """LiftingSurface."""

    def __init__(
        self,
        p: bullet_client.BulletClient,
        physics_period: float,
        np_random: np.random.RandomState,
        uav_id: int,
        surface_id: int,
        command_id: None | int,
        command_sign: float,
        lifting_unit: np.ndarray,
        forward_unit: np.ndarray,
        Cl_alpha_2D: float,
        chord: float,
        span: float,
        flap_to_chord: float,
        eta: float,
        alpha_0_base: float,
        alpha_stall_P_base: float,
        alpha_stall_N_base: float,
        Cd_0: float,
        deflection_limit: float,
        tau: float,
    ):
        """Used for simulating a single lifting surface.

        Args:
            p (bullet_client.BulletClient): p
            physics_period (float): physics_period
            np_random (np.random.RandomState): np_random
            uav_id (int): uav_id
            surface_id (int): surface_id
            command_id (None | int): command_id, for convenience
            command_sign (float): command_sign, for convenience
            lifting_unit (np.ndarray): (3,) unit vector representing the direction of lift
            forward_unit (np.ndarray): (3,) unit vector representing the direction of travel
            Cl_alpha_2D (float): float
            chord (float): float
            span (float): float
            flap_to_chord (float): float
            eta (float): float
            alpha_0_base (float): float
            alpha_stall_P_base (float): float
            alpha_stall_N_base (float): float
            Cd_0 (float): float
            deflection_limit (float): float
            tau (float): float
        """
        self.p = p
        self.physics_period = physics_period
        self.np_random = np_random

        # store IDs
        self.uav_id = uav_id
        self.surface_id = surface_id

        # command inputs for referencing
        self.command_id = command_id
        self.command_sign = command_sign

        # some checks for the lifting and norm vectors
        assert lifting_unit.shape == (3,)
        assert forward_unit.shape == (3,)
        assert (
            tau >= 0.0 / physics_period
        ), f"Setting `tau = 1 / physics_period` is equivalent to 0, 0 is not a valid option, got {tau}."
        if np.linalg.norm(lifting_unit) != 1.0:
            warnings.warn(f"Norm of `{lifting_unit=}` is not 1.0, normalizing...")
            lifting_unit /= np.linalg.norm(lifting_unit)
        if np.linalg.norm(forward_unit) != 1.0:
            warnings.warn(f"Norm of `{forward_unit=}` is not 1.0, normalizing...")
            forward_unit /= np.linalg.norm(forward_unit)
        if np.dot(lifting_unit, forward_unit) != 0.0:
            warnings.warn(
                f"`{forward_unit}` and `{lifting_unit}` are not orthogonal, you have been warned..."
            )

        # get the lift, drag, and torque units
        self.lift_unit = lifting_unit
        self.drag_unit = forward_unit
        self.torque_unit = np.cross(lifting_unit, forward_unit)

        # wing parameters
        self.Cl_alpha_2D = Cl_alpha_2D
        self.chord = chord
        self.span = span
        self.flap_to_chord = flap_to_chord
        self.eta = eta
        self.alpha_0_base = alpha_0_base
        self.alpha_stall_P_base = alpha_stall_P_base
        self.alpha_stall_N_base = alpha_stall_N_base
        self.Cd_0 = Cd_0
        self.deflection_limit = deflection_limit
        self.cmd_tau = tau

        # precompute some constants
        self.half_rho = 0.5 * 1.225
        self.area = self.chord * self.span
        self.aspect = self.span / self.chord
        self.alpha_stall_P_base = np.deg2rad(self.alpha_stall_P_base)
        self.alpha_stall_N_base = np.deg2rad(self.alpha_stall_N_base)
        self.alpha_0_base = np.deg2rad(self.alpha_0_base)
        self.Cl_alpha_3D = self.Cl_alpha_2D * (
            self.aspect
            / (self.aspect + ((2.0 * (self.aspect + 4.0)) / (self.aspect + 2.0)))
        )
        self.theta_f = np.arccos(2.0 * self.flap_to_chord - 1.0)
        self.aero_tau = 1 - ((self.theta_f - np.sin(self.theta_f)) / np.pi)

        # runtime parameters
        self.local_surface_velocity = np.array([0.0, 0.0, 0.0])

    def reset(self):
        """Reset the lifting surfaces."""
        self.actuation = 0.0

    def get_states(self) -> float:
        """Gets the current state of the components.

        Returns:
            float: the level of deflection of the surface.
        """
        return self.actuation

    def state_update(self, surface_velocity: np.ndarray):
        """Updates the local surface velocity of the lifting surface.

        Args:
            surface_velocity (np.ndarray): surface_velocity
        """
        self.local_surface_velocity = surface_velocity

    def physics_update(self, cmd: float):
        """Converts a commanded actuation state into forces on the lifting surface.

        Args:
            cmd (float): normalized actuation in [-1, 1]

        Returns:
            tuple[np.ndarray, np.ndarray]: vec3 force, vec3 torque
        """
        freestream_speed = np.linalg.norm(self.local_surface_velocity)
        lifting_airspeed = np.dot(self.local_surface_velocity, self.lift_unit)
        forward_airspeed = np.dot(self.local_surface_velocity, self.drag_unit)
        alpha = np.arctan2(-lifting_airspeed, forward_airspeed)

        # model the deflection using first order ODE, y' = T/tau * (setpoint - y)
        self.actuation += (self.physics_period / self.cmd_tau) * (cmd - self.actuation)

        # compute aerofoil parameters
        [Cl, Cd, CM] = self._compute_aero_data(alpha)

        Q = self.half_rho * np.square(freestream_speed)  # Dynamic pressure
        Q_area = Q * self.area

        lift = Cl * Q_area
        drag = Cd * Q_area
        force_normal = (lift * np.cos(alpha)) + (drag * np.sin(alpha))
        force_parallel = (lift * np.sin(alpha)) - (drag * np.cos(alpha))

        force = self.lift_unit * force_normal + self.drag_unit * force_parallel
        torque = Q_area * CM * self.chord * self.torque_unit

        self.p.applyExternalForce(
            self.uav_id,
            self.surface_id,
            force,
            [0.0, 0.0, 0.0],
            self.p.LINK_FRAME,
        )
        self.p.applyExternalTorque(
            self.uav_id, self.surface_id, torque, self.p.LINK_FRAME
        )

    def _compute_aero_data(self, alpha: float) -> tuple[float, float, float]:
        """Computes the relevant aerodynamic data depending on the current state of the lifting surface.

        Args:
            deflection (float): deflection of the lifting surface in degrees
            alpha (float): angle of attack in degrees

        Returns:
            tuple[float, float, float]: Cl, Cd, CM
        """
        # deflection must be in degrees because engineering uses degrees
        deflection_radians = np.deg2rad(self.actuation * self.deflection_limit)

        delta_Cl = self.Cl_alpha_3D * self.aero_tau * self.eta * deflection_radians
        delta_Cl_max = self.flap_to_chord * delta_Cl
        Cl_max_P = (
            self.Cl_alpha_3D * (self.alpha_stall_P_base - self.alpha_0_base)
            + delta_Cl_max
        )
        Cl_max_N = (
            self.Cl_alpha_3D * (self.alpha_stall_N_base - self.alpha_0_base)
            + delta_Cl_max
        )
        alpha_0 = self.alpha_0_base - (delta_Cl / self.Cl_alpha_3D)
        alpha_stall_P = alpha_0 + (Cl_max_P / self.Cl_alpha_3D)
        alpha_stall_N = alpha_0 + (Cl_max_N / self.Cl_alpha_3D)

        # no stall condition
        if alpha_stall_N < alpha and alpha < alpha_stall_P:
            Cl = self.Cl_alpha_3D * (alpha - alpha_0)
            alpha_i = Cl / (np.pi * self.aspect)
            alpha_eff = alpha - alpha_0 - alpha_i
            CT = self.Cd_0 * np.cos(alpha_eff)
            CN = (Cl + (CT * np.sin(alpha_eff))) / np.cos(alpha_eff)
            Cd = (CN * np.sin(alpha_eff)) + (CT * np.cos(alpha_eff))
            CM = -CN * (0.25 - (0.175 * (1.0 - ((2.0 * alpha_eff) / np.pi))))

            return Cl, Cd, CM

        # positive stall
        if alpha > 0.0:
            # Stall calculations to find alpha_i at stall
            Cl_stall = self.Cl_alpha_3D * (alpha_stall_P - alpha_0)
            alpha_i_at_stall = Cl_stall / (np.pi * self.aspect)
            # alpha_i post-stall Pos
            alpha_i = np.interp(
                alpha, [alpha_stall_P, np.pi / 2.0], [alpha_i_at_stall, 0.0]
            )
        # negative stall
        else:
            # Stall calculations to find alpha_i at stall
            Cl_stall = self.Cl_alpha_3D * (alpha_stall_N - alpha_0)
            alpha_i_at_stall = Cl_stall / (np.pi * self.aspect)
            # alpha_i post-stall Neg
            alpha_i = np.interp(
                alpha, [-np.pi / 2.0, alpha_stall_N], [0.0, alpha_i_at_stall]
            )

        alpha_eff = alpha - alpha_0 - alpha_i

        # Drag coefficient at 90 deg dependent on deflection angle
        Cd_90 = (
            ((-4.26 * (10**-2)) * (deflection_radians**2))
            + ((2.1 * (10**-1)) * deflection_radians)
            + 1.98
        )
        CN = (
            Cd_90
            * np.sin(alpha_eff)
            * (
                1.0 / (0.56 + 0.44 * abs(np.sin(alpha_eff)))
                - 0.41 * (1.0 - np.exp(-17.0 / self.aspect))
            )
        )
        CT = 0.5 * self.Cd_0 * np.cos(alpha_eff)
        Cl = (CN * np.cos(alpha_eff)) - (CT * np.sin(alpha_eff))
        Cd = (CN * np.sin(alpha_eff)) + (CT * np.cos(alpha_eff))
        CM = -CN * (0.25 - (0.175 * (1.0 - ((2.0 * abs(alpha_eff)) / np.pi))))

        return Cl, Cd, CM
