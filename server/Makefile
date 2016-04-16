TARGET  = ultraGarden
CXX     = g++
LFLAGS  = -L/usr/local/lib -lwiringPi -lcurl
WARNCXXFLAGS= -Wall -Wextra -Wshadow -Weffc++ -Wstrict-aliasing -ansi -pedantic
WARNLFLAGS  = 

BUILD	= debug
ifeq ($(BUILD),debug)
	CXXFLAGS= -g3 -ggdb -O0 -DDEBUG -std=gnu++1y -fstack-protector
else
	CXXFLAGS= -g3 -O3 -std=gnu++1y
endif

rwildcard	= $(foreach d,$(wildcard $1*),$(call rwildcard,$d/,$2) $(filter $(subst *,%,$2),$d))
ALL_SOURCES = $(call rwildcard,,*.cpp)
EXTLIBS_OBJ	= extlib/c-log/src/log.o
TEST_SOURCES= $(filter %_test.cpp,$(ALL_SOURCES))
SOURCES		= $(filter-out %_test.cpp,$(ALL_SOURCES))
OBJECTS     = $(SOURCES:.cpp=.o) $(EXTLIBS_OBJ)
DEPFILES    = $(SOURCES:.cpp=.d) $(EXTLIBS_OBJ:.o=.d)
TEST_TARGETS= $(subst .cpp,,$(TEST_SOURCES))


$(TARGET): $(OBJECTS)
	$(CXX) $(WARNCXXFLAGS) $(WARNLFLAGS) $(CXXFLAGS) -o $(TARGET) $(OBJECTS) $(LFLAGS)

tests: $(TEST_TARGETS)

all: $(TARGET) $(TEST_TARGETS)


%.o: %.cpp
	$(CXX) -MMD $(WARNCXXFLAGS) $(CXXFLAGS) -o $@ -c $<

%: %_test.cpp
	$(CXX) -MMD $(WARNCXXFLAGS) $(CXXFLAGS) -o $@ -c $<

extlib/c-log/src/log.o: extlib/c-log/src/log.c
	$(CXX) -MMD $(WARNCXXFLAGS) $(CXXFLAGS) -o $@ -c $<

clean:
	rm -f $(DEPFILES) $(OBJECTS) $(TARGET) $(TEST_TARGETS)

