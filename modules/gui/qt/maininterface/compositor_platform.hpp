/* Modified 2026-10-24: macOS accessibility and build compatibility. */
/*****************************************************************************
 * Copyright (C) 2024 VLC authors and VideoLAN
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
 *****************************************************************************/
#ifndef COMPOSITOR_PLATFORM_HPP
#define COMPOSITOR_PLATFORM_HPP

#include "compositor.hpp"
#include "compositor_accessibility.hpp"

#include <QWindow>
#include <QPointer>
#include <QQuickWindow>

#include <memory>

class QQuickView;

namespace vlc {

// The platform compositor renders its QML interface in a child window. Expose
// that scene through the real top-level window for macOS accessibility clients.
class CompositorPlatformRootWindow : public QWindow, public AccessibleRenderWindow
{
    Q_OBJECT
public:
    QPointer<QQuickWindow> accessibleWindow;
    QQuickWindow *getOffscreenWindow() const override { return accessibleWindow; }
#if QT_CONFIG(accessibility)
    QAccessibleInterface *accessibleRoot() const override;
#endif
    QObject *focusObject() const override
    {
        return accessibleWindow ? accessibleWindow->focusObject() : QWindow::focusObject();
    }
};

class CompositorPlatform : public CompositorVideo
{
    Q_OBJECT

public:
    CompositorPlatform(qt_intf_t *p_intf, QObject* parent = nullptr);

    bool init() override;

    bool makeMainInterface(MainCtx *, std::function<void(QQuickWindow*)> aboutToShowQuickWindowCallback = {}) override;
    void destroyMainInterface() override;
    void unloadGUI() override;
    bool setupVoutWindow(vlc_window_t*, VoutDestroyCb destroyCb) override;
    QWindow* interfaceMainWindow() const override;
    QQuickWindow* quickWindow() const override;
    Type type() const override;
    QQuickItem * activeFocusItem() const override;

    bool eventFilter(QObject *watched, QEvent *event) override;

protected:
    bool canDoCombinedSurfaceUpdates() const override { return true; };
    void commitSurface() override;

private:
    int windowEnable(const vlc_window_cfg_t *) override;
    void windowDisable() override;

private slots:
    void onSurfacePositionChanged(const QPointF& position) override;
    void onSurfaceSizeChanged(const QSizeF& size) override;

private:
    std::unique_ptr<CompositorPlatformRootWindow> m_rootWindow;
    QPointer<QWindow> m_videoWindow;
    QPointer<QQuickView> m_quickWindow;

    std::optional<QSize> m_pendingSize;
    std::optional<QPoint> m_pendingPosition;
};

}

#endif // COMPOSITOR_PLATFORM_HPP
