from conans import ConanFile, CMake, tools
import os

class CatkinConan(ConanFile):
    name = "catkin"
    version = "0.6.19"
    license = "BSD"
    url = "https://github.com/sbarthelemy/conan-toolchain"
    description = "Low-level build system macros and infrastructure for ROS."
    settings = "os", "compiler", "build_type", "arch" #TODO?
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/ros/catkin.git --branch {}".format(self.version))

    def build(self):
        cmake = CMake(self)
        self.run('cmake catkin %s -DCMAKE_INSTALL_PREFIX="%s"'
                % (cmake.command_line, self.package_folder))
        self.run("cmake --build . --target install %s" % cmake.build_config)

    def package(self):
        pass

    def package_info(self):
        pass
