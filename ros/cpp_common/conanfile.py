from conans import ConanFile, CMake, tools
import os

class CppcommonConan(ConanFile):
    name = "cpp_common"
    version = "0.5.8"
    license = "BSD"
    url = "https://github.com/sbarthelemy/conan-toolchain"
    description = "cpp_common contains C++ code for doing things that are"\
                  " not necessarily ROS related, but are useful for multiple"\
                  " packages."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    build_requires = "catkin/0.6.19@sbarthelemy/testing"
    requires = "Boost /1.59.0@lasote/stable",\
               "console_bridge/0.2.5@sbarthelemy/testing"

    def source(self):
        self.run("git clone https://github.com/ros/roscpp_core.git --branch {}".format(self.version))
        tools.replace_in_file("roscpp_core/cpp_common/CMakeLists.txt",
               "project(cpp_common)",
               "project(cpp_common)\n" \
               "include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\n" \
               "conan_basic_setup()")

    def imports(self):
       self.copy("*.dll", "", "bin")
       self.copy("*.dylib", "", "lib")

    def build(self):
        cmake = CMake(self)
        self.run('cmake roscpp_core/cpp_common %s -DCMAKE_INSTALL_PREFIX="%s"'
                % (cmake.command_line, self.package_folder))
        self.run("cmake --build . --target install %s" % cmake.build_config)

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = ["cpp_common"]
