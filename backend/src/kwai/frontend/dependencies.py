"""Module for defining dependencies for the frontend applications."""

from pathlib import Path
from typing import Annotated

from fastapi import Depends, HTTPException, status

from kwai.core.settings import Settings, get_settings
from kwai.frontend.vite import DevelopmentVite, ProductionVite, Vite


class ViteDependency:
    """Vite is a dependency."""

    def __init__(self, application_name: str):
        self._application_name = application_name

    def __call__(self, settings: Annotated[Settings, Depends(get_settings)]) -> Vite:
        """Create a Vite environment for this application."""
        if not hasattr(settings.frontend.apps, self._application_name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Application {self._application_name} does not exist.",
            )

        app_setting = getattr(settings.frontend.apps, self._application_name)
        if settings.frontend.test:
            if app_setting.server is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Setting 'server' not set for application {self._application_name}",
                )
            if app_setting.base is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Setting 'base' not set for application {self._application_name}",
                )
            return DevelopmentVite(app_setting.server, app_setting.base)

        manifest_path = (
            Path(settings.frontend.path)
            / "apps"
            / self._application_name
            / "dist"
            / ".vite"
            / "manifest.json"
        )
        if not manifest_path.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Manifest file {manifest_path} not found",
            )

        return ProductionVite(
            manifest_path,
            Path(settings.frontend.path) / "apps" / self._application_name,
        )
