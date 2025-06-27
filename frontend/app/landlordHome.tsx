import React, { useState, useEffect } from "react";
import {
    View,
    Text,
    Image,
    ScrollView,
    StyleSheet,
    TouchableOpacity,
    Alert,
    ActivityIndicator,
} from "react-native";
import { useAuth } from "./context/AuthContext";
import { useNavigation } from "@react-navigation/native";
import useAxios from "./hooks/useAxios";
import { useIsFocused } from "@react-navigation/native";
import useUser from "./hooks/useUser";
import { useRouter } from "expo-router";
import { LandlordHomeStackParamList } from "./stacks/landlordHomeStack";
import { StackNavigationProp } from "@react-navigation/stack";
import { Ionicons } from "@expo/vector-icons";

type LandlordHomeScreenNavigationProp = StackNavigationProp<LandlordHomeStackParamList, "home">;

export default function LandlordHomeScreen() {
    const [groups, setGroups] = useState<any>([]);
    const [properties, setProperties] = useState<any>([]);
    const [loadingState, setLoadingState] = useState(true); // Custom loading state

    const { user, userError } = useUser();
    const { logout } = useAuth();
    const { get, error, loading } = useAxios();
    const isFocused = useIsFocused();
    const navigation = useNavigation<LandlordHomeScreenNavigationProp>();
    const router = useRouter();

    useEffect(() => {
        if (isFocused) {
            loadData();
        }
    }, [isFocused]);

    useEffect(() => {
        if (error) {
            Alert.alert("Error", error);
        }
    }, [error]);

    const loadData = async () => {
        setLoadingState(true);
        await Promise.all([fetchGroups(), fetchProperties()]);
        setLoadingState(false);
    };

    const fetchGroups = async () => {
        const response = await get<any>("/api/groups/landlord");
        if (response) {
            setGroups(response.data);
        }
    };

    const fetchProperties = async () => {
        const response = await get<any>("/api/properties/");
        if (response) {
            setProperties(response.data);
        }
    };

    const handleNavigateToAddGroup = () => {
        navigation.navigate("addGroup");
    };

    const handleNavigateToAddProperty = () => {
        navigation.navigate("addProperty");
    };

    const handleNavigateToEditProperty = (propertyId: string) => {
        navigation.navigate("viewEditProperty", { propertyId });
    };

    const handleNavigateToGroup = (groupId: string) => {
        router.push({ pathname: "/groupNavigation", params: { groupId, role: "landlord" } });
    };

    const handleNavigateToManageGroup = (groupId: string) => {
        navigation.navigate("editGroup", { groupId });
    };

    const handleLogout = async () => {
        await logout();
        router.push("/login");
    };

    if (loadingState) {
        return (
            <View style={styles.loadingContainer}>
                <ActivityIndicator size="large" color="#0000ff" />
            </View>
        );
    }

    if (userError) return <Text>Error: {userError}</Text>;
    if (!user) return <Text>No user found.</Text>;

    // Group the groups into rows of two
    const groupRows = [];
    for (let i = 0; i < groups.length; i += 2) {
        groupRows.push(groups.slice(i, i + 2));
    }

    // Group properties into rows of two (for the properties section)
    const propertyRows = [];
    for (let i = 0; i < properties.length; i += 2) {
        propertyRows.push(properties.slice(i, i + 2));
    }

    return (
        <View style={styles.root}>
            {/* Sticky Header */}
            <View style={styles.screenHeader}>
                <Text style={styles.screenHeaderTitle}>Home</Text>
            </View>

            <ScrollView contentContainerStyle={styles.container}>
                {/* Profile Section */}
                <View style={styles.profileSection}>
                    <Image
                        style={styles.profileImage}
                        source={{
                            uri: "https://www.gravatar.com/avatar/00000000000000000000000000000000?s=200&d=mp",
                        }}
                    />
                    <View style={styles.profileInfo}>
                        <Text style={styles.welcomeText}>
                            Welcome {user.firstName}, {user.lastName}
                        </Text>
                        <Text style={styles.emailText}>{user.email}</Text>
                    </View>
                </View>

                <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
                    <Text style={styles.logoutText}>Logout</Text>
                </TouchableOpacity>

                <View style={styles.mainContent}>
                    {/* Groups Section */}
                    <View style={styles.section}>
                        <Text style={styles.sectionTitle}>Manage Groups</Text>
                        <TouchableOpacity style={styles.createButton} onPress={handleNavigateToAddGroup}>
                            <Text style={styles.buttonText}>Create New Group</Text>
                        </TouchableOpacity>

                        {/* Render groups in rows of two */}
                        <View style={styles.groupsGrid}>
                            {groupRows.map((row, rowIndex) => (
                                <View key={rowIndex} style={styles.groupRow}>
                                    {row.map((group: any) => (
                                        <TouchableOpacity
                                            key={group.id}
                                            style={styles.groupCard}
                                            onPress={() => handleNavigateToGroup(group.id)}
                                        >
                                            <Text style={styles.groupCardTitle}>{group.name}</Text>
                                            {group.property && group.property.exteriorImage ? (
                                                <Image
                                                    style={styles.groupPropertyImage}
                                                    source={{ uri: group.property.exteriorImage }}
                                                />
                                            ) : (
                                                <View style={styles.noImagePlaceholder}>
                                                    <Text style={styles.noImageText}>No Image</Text>
                                                </View>
                                            )}
                                            {group.property && (
                                                <View style={styles.groupPropertyDetails}>
                                                    <Text style={styles.groupPropertyName}>{group.property.name}</Text>
                                                    <Text style={styles.groupPropertyAddress}>
                                                        {group.property.address}, {group.property.city}
                                                    </Text>
                                                </View>
                                            )}
                                            <TouchableOpacity style={styles.editButton} onPress={() => handleNavigateToManageGroup(group.id)}>
                                                <Text style={styles.buttonText}>Edit Group</Text>
                                            </TouchableOpacity>
                                        </TouchableOpacity>
                                    ))}
                                    {row.length === 1 && <View style={[styles.groupCard, { width: "48%" }]} />}
                                </View>
                            ))}
                        </View>
                    </View>

                    {/* Properties Section */}
                    <View style={styles.section}>
                        <Text style={styles.sectionTitle}>Manage Properties</Text>
                        <TouchableOpacity style={styles.createButton} onPress={handleNavigateToAddProperty}>
                            <Text style={styles.buttonText}>Create New Property</Text>
                        </TouchableOpacity>

                        {/* Render properties in rows */}
                        <View style={styles.propertiesGrid}>
                            {propertyRows.map((row, rowIndex) => (
                                <View key={rowIndex} style={styles.propertyRow}>
                                    {row.map((property: any) => (
                                        <View key={property.id} style={styles.propertyCard}>
                                            <Image style={styles.propertyImage} source={{ uri: property.exteriorImage }} />
                                            <View style={styles.propertyDetails}>
                                                <Text style={styles.propertyName}>{property.name}</Text>
                                                <Text style={styles.propertyAddress}>
                                                    {property.address}, {property.city}
                                                </Text>
                                                <TouchableOpacity style={styles.editButton} onPress={() => handleNavigateToEditProperty(property.id)}>
                                                    <Text style={styles.buttonText}>View/Edit Details</Text>
                                                </TouchableOpacity>
                                            </View>
                                        </View>
                                    ))}
                                    {row.length === 1 && <View style={[styles.propertyCard, { width: "48%" }]} />}
                                </View>
                            ))}
                        </View>
                    </View>
                </View>
            </ScrollView>
        </View>
    );
}

const styles = StyleSheet.create({
    root: {
        flex: 1,
        backgroundColor: "#f5f5f5",
    },
    screenHeader: {
        backgroundColor: "white",
        paddingTop: 50,
        paddingBottom: 10,
        borderBottomWidth: 1,
        borderBottomColor: "#ddd",
        elevation: 3,
        alignItems: "center",
    },
    screenHeaderTitle: {
        fontSize: 22,
        fontWeight: "bold",
    },
    loadingContainer: {
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
        backgroundColor: "#f5f5f5",
    },
    container: {
        flexGrow: 1,
        padding: 16,
    },
    profileSection: {
        flexDirection: "row",
        alignItems: "center",
        backgroundColor: "white",
        padding: 20,
        borderRadius: 8,
        marginBottom: 20,
    },
    profileImage: {
        width: 60,
        height: 60,
        borderRadius: 30,
        marginRight: 15,
    },
    profileInfo: {
        flex: 1,
    },
    welcomeText: {
        fontSize: 18,
        fontWeight: "bold",
    },
    emailText: {
        fontSize: 14,
        color: "#666",
    },
    logoutButton: {
        backgroundColor: "#ff4444",
        padding: 10,
        borderRadius: 6,
        marginBottom: 20,
        alignSelf: "center",
        minWidth: 100,
        alignItems: "center",
    },
    logoutText: {
        color: "white",
        fontWeight: "600",
    },
    mainContent: {
        gap: 20,
    },
    section: {
        backgroundColor: "white",
        padding: 20,
        borderRadius: 8,
        elevation: 3,
        marginBottom: 20,
    },
    sectionTitle: {
        fontSize: 20,
        fontWeight: "bold",
        marginBottom: 15,
    },
    createButton: {
        backgroundColor: "#4CAF50",
        padding: 12,
        borderRadius: 6,
        alignItems: "center",
        marginBottom: 15,
    },
    buttonText: {
        color: "white",
        fontWeight: "600",
    },
    // Groups Grid Styles
    groupsGrid: {
        // Container for group rows
    },
    groupRow: {
        flexDirection: "row",
        justifyContent: "space-between",
        marginBottom: 15,
    },
    groupCard: {
        backgroundColor: "#fff",
        borderRadius: 8,
        width: "48%",
        marginBottom: 15,
        elevation: 3,
        padding: 10,
    },
    groupCardTitle: {
        fontSize: 18,
        fontWeight: "bold",
        marginBottom: 10,
        textAlign: "center",
    },
    groupPropertyImage: {
        width: "100%",
        height: 150,
        borderRadius: 8,
        marginBottom: 10,
    },
    noImagePlaceholder: {
        width: "100%",
        height: 150,
        borderRadius: 8,
        backgroundColor: "#ddd",
        justifyContent: "center",
        alignItems: "center",
        marginBottom: 10,
    },
    noImageText: {
        color: "#666",
        fontSize: 16,
    },
    groupPropertyDetails: {
        alignItems: "center",
    },
    groupPropertyName: {
        fontSize: 16,
        fontWeight: "bold",
    },
    groupPropertyAddress: {
        fontSize: 14,
        color: "#666",
    },
    // Properties Section (kept as before)
    propertiesGrid: {
        // Using our grouped rows approach; handled in propertyRow
    },
    propertyRow: {
        flexDirection: "row",
        justifyContent: "space-between",
        marginBottom: 15,
    },
    propertyCard: {
        backgroundColor: "#f9f9f9",
        borderRadius: 8,
        overflow: "hidden",
        width: "48%",
        marginBottom: 15,
    },
    propertyImage: {
        width: "100%",
        height: 150,
    },
    propertyDetails: {
        padding: 15,
        gap: 8,
    },
    propertyName: {
        fontSize: 16,
        fontWeight: "600",
    },
    propertyAddress: {
        fontSize: 14,
        color: "#666",
    },
    propertyCity: {
        fontSize: 14,
        color: "#666",
    },
    // Common editButton style for group and property cards
    editButton: {
        backgroundColor: "#2196F3",
        padding: 8,
        borderRadius: 6,
        alignItems: "center",
        marginTop: 10,
    },
});