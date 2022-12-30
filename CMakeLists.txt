project(DockingInterface)

include(ExternalProject)

if (QVINA OR VINA OR SMINA)
else()
    set(QVINA true)
    set(VINA true)
    set(SMINA true)
endif()

if (QVINA)
    if(BOOST_ROOT)
        ExternalProject_Add(
                qvina
                SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/handlers/qvina"
                PREFIX qvina
                INSTALL_COMMAND ""
                CMAKE_ARGS -DBOOST_ROOT=${BOOST_ROOT} -DBUILD_SUB_CMAKE=true
        )
    else()
        ExternalProject_Add(
                qvina
                SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/handlers/qvina"
                PREFIX qvina
                INSTALL_COMMAND ""
                CMAKE_ARGS -DBUILD_SUB_CMAKE=true
        )
    endif()

endif()

if (SMINA)
    if (OPENBABEL3_ROOT AND BOOST_ROOT)
        ExternalProject_Add(
                smina
                SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/handlers/smina"
                PREFIX smina
                INSTALL_COMMAND ""
                CMAKE_ARGS -DBOOST_ROOT=${BOOST_ROOT} -DOPENBABEL3_ROOT=${OPENBABEL3_ROOT} -DBUILD_SUB_CMAKE=true
        )
    elseif(OPENBABEL2_ROOT AND BOOST_ROOT)
        ExternalProject_Add(
                smina
                SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/handlers/smina"
                PREFIX smina
                INSTALL_COMMAND ""
                CMAKE_ARGS -DBOOST_ROOT=${BOOST_ROOT} -DOPENBABEL2_ROOT=${OPENBABEL2_ROOT} -DBUILD_SUB_CMAKE=true
        )
    elseif(OPENBABEL2_ROOT)
        ExternalProject_Add(
                smina
                SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/handlers/smina"
                PREFIX smina
                INSTALL_COMMAND ""
                CMAKE_ARGS -DOPENBABEL2_ROOT=${OPENBABEL2_ROOT} -DBUILD_SUB_CMAKE=true
        )
    elseif(OPENBABEL3_ROOT)
        ExternalProject_Add(
                smina
                SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/handlers/smina"
                PREFIX smina
                INSTALL_COMMAND ""
                CMAKE_ARGS -DOPENBABEL3_ROOT=${OPENBABEL3_ROOT} -DBUILD_SUB_CMAKE=true
        )
    elseif(BOOST_ROOT)
        ExternalProject_Add(
                smina
                SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/handlers/smina"
                PREFIX smina
                INSTALL_COMMAND ""
                CMAKE_ARGS -DBOOST_ROOT=${BOOST_ROOT} -DBUILD_SUB_CMAKE=true
        )
    else()
        ExternalProject_Add(
                smina
                SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/handlers/smina"
                PREFIX smina
                INSTALL_COMMAND ""
                CMAKE_ARGS -DBUILD_SUB_CMAKE=true
        )
    endif()
endif()

if (VINA)
    if(BOOST_ROOT)
        ExternalProject_Add(
                vina
                SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/handlers/vina"
                PREFIX vina
                INSTALL_COMMAND ""
                CMAKE_ARGS -DBOOST_ROOT=${BOOST_ROOT} -DBUILD_SUB_CMAKE=true
        )
    else()
        ExternalProject_Add(
                vina
                SOURCE_DIR "${CMAKE_CURRENT_SOURCE_DIR}/handlers/vina"
                PREFIX vina
                INSTALL_COMMAND ""
                CMAKE_ARGS -DBUILD_SUB_CMAKE=true
        )
    endif()
endif()



