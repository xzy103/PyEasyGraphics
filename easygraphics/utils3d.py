from PyQt5.QtGui import QMatrix4x4, QVector3D
import math

__all__ = ['ortho_look_at', 'ortho_45']


def ortho_45():
    return ortho_look_at(1, 1, 1, -1, -1, 1)


def ortho_look_at(eye_x: float, eye_y: float, eye_z: float,
                  up_x: float, up_y: float, up_z: float):
    eye = QVector3D(eye_x, eye_y, eye_z)
    up = QVector3D(up_x, up_y, up_z)
    center = QVector3D(0, 0, 0)
    view = center - eye
    right = QVector3D.crossProduct(up, eye)
    z_axis = QVector3D(0, 0, 1)
    # 求 up 到 z轴的投影
    up_project_z_factor = QVector3D.dotProduct(up, z_axis) / z_axis.lengthSquared()
    up_project_z = z_axis * up_project_z_factor
    # 求 z轴 和 up到z轴投影之间的夹角
    cos_up_and_z = QVector3D.dotProduct(z_axis, up_project_z) / z_axis.length() / up_project_z.length()
    angle_up_and_z = math.acos(cos_up_and_z)
    cos_x = math.cos(angle_up_and_z)
    sin_x = math.sin(angle_up_and_z)
    m_x = QMatrix4x4(1, 0, 0, 0,
                     0, cos_x, -sin_x, 0,
                     0, sin_x, cos_x, 0,
                     0, 0, 0, 1)
    # print(angle_up_and_z)
    # print(m_x)

    # 求视线矢量到z轴的投影
    eye_project_z_factor = QVector3D.dotProduct(eye, z_axis) / z_axis.lengthSquared()
    eye_project_z = z_axis * eye_project_z_factor
    # 视线矢量在xy平面上的投影
    eye_project_xy = eye - eye_project_z
    # 求视线矢量与xy平面的夹角
    cos_eye_and_xy = QVector3D.dotProduct(eye, eye_project_xy) / eye_project_xy.length() / eye.length()
    angle_eye_and_xy = math.acos(cos_eye_and_xy)
    if eye.z() < 0:
        angle_eye_and_xy = - angle_eye_and_xy

    # 求 视线矢量在xy平面上的投影 与 x轴夹角
    x_axis = QVector3D(1, 0, 0)
    cos_project_xy_and_x = QVector3D.dotProduct(x_axis, eye_project_xy) / x_axis.length() / eye_project_xy.length()
    angle_project_xy_and_x = math.acos(cos_project_xy_and_x)
    if eye_project_xy.y() < 0:
        angle_project_xy_and_x = 2 * math.pi - angle_project_xy_and_x

    # print("eye", eye)
    # print("eye_project_z", eye_project_z)
    # print("eye_project_xy", eye_project_xy)
    # print(angle_eye_and_xy)
    # print(angle_project_xy_and_x)

    # 绕y轴逆时针旋转 angle_eye_and_xy 度
    cos_1 = math.cos(angle_eye_and_xy)
    sin_1 = math.sin(angle_eye_and_xy)
    m_y = QMatrix4x4(cos_1, 0, sin_1, 0,
                     0, 1, 0, 0,
                     sin_1, 0, cos_1, 0,
                     0, 0, 0, 1)
    # 绕z轴顺时针转 angle_project_xy_and_x 度
    cos_2 = math.cos(-angle_project_xy_and_x)
    sin_2 = math.sin(-angle_project_xy_and_x)
    m_z = QMatrix4x4(-cos_2, sin_2, 0, 0,
                     sin_2, cos_2, 0, 0,
                     0, 0, 1, 0,
                     0, 0, 0, 1)

    m_ortho = QMatrix4x4(0, 1, 0, 0,
                         0, 0, -1, 0,
                         0, 0, 0, 0,
                         0, 0, 0, 1)

    return m_ortho * m_x.transposed() * m_y.transposed() * m_z.transposed()