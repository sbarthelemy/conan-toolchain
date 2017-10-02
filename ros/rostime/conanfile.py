from conans import ConanFile, CMake, tools
import os

class RostimeConan(ConanFile):
    name = "rostime"
    version = "0.5.8"
    license = "BSD"
    url = "https://github.com/sbarthelemy/conan-toolchain"
    description = "Time and Duration implementations for C++ libraries," \
                  " including roscpp."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    build_requires = "catkin/0.6.19@sbarthelemy/testing"
    requires = "Boost /1.59.0@lasote/stable",\
               "cpp_common/0.5.8@sbarthelemy/testing"

    def source(self):
        self.run("git clone https://github.com/ros/roscpp_core.git --branch {}".format(self.version))
        tools.replace_in_file("roscpp_core/rostime/CMakeLists.txt",
               "project(rostime)",
               "project(rostime)\n" \
               "include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)\n" \
               "conan_basic_setup()")

    def imports(self):
       self.copy("*.dll", "", "bin")
       self.copy("*.dylib", "", "lib")

    def build(self):
        cmake = CMake(self)
        self.run('cmake roscpp_core/rostime %s -DCMAKE_INSTALL_PREFIX="%s"'
                % (cmake.command_line, self.package_folder))
        self.run("cmake --build . --target install %s" % cmake.build_config)

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = ["rostime"]
