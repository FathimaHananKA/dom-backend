from rest_framework import serializers
from .models import Dormitory
from rooms.models import Room

class DormitorySerializer(serializers.ModelSerializer):
    warden_name = serializers.CharField(source='assigned_warden.user.username', read_only=True)
    room_configurations = serializers.ListField(
        child=serializers.DictField(), 
        write_only=True, 
        required=False
    )
    # Calculate totals dynamically from actual Room and Bed counts
    total_rooms = serializers.SerializerMethodField()
    total_beds = serializers.SerializerMethodField()
    
    class Meta:
        model = Dormitory
        fields = ['id', 'name', 'gender', 'total_rooms', 'total_beds', 'assigned_warden', 'warden_name', 'room_prefix', 'room_configurations']
        read_only_fields = ['warden_name', 'total_rooms', 'total_beds']
    
    def get_total_rooms(self, obj):
        """Calculate total rooms by counting actual Room objects"""
        from rooms.models import Room
        return Room.objects.filter(dormitory=obj).count()
    
    def get_total_beds(self, obj):
        """Calculate total beds by counting actual Bed objects"""
        from rooms.models import Bed, Room
        # Count all beds in rooms that belong to this dormitory
        return Bed.objects.filter(room__dormitory=obj).count()

    def _process_room_configurations(self, instance, configurations):
        """
        Helper to create Rooms and Beds from configurations.
        """
        if not configurations:
            return

        rooms_to_create = []
        
        CAPACITY_MAP = {
            'single': 1,
            'double': 2,
            'triple': 3,
        }
        
        from rooms.models import Bed # Local import to avoid circular if any
        
        for config in configurations:
            # Frontend sends 'startName', manual might send 'prefix'
            # Default to 'R' if neither found
            raw_prefix = config.get('startName') or config.get('prefix') or 'R'
            
            # Validate/Truncate prefix length (max 8 to allow for digits)
            # Room number max_length=10
            prefix = raw_prefix[:8]
                
            count = int(config.get('count', 0))
            rtype = config.get('type', 'double').lower()
            capacity = CAPACITY_MAP.get(rtype, 2)
            
            for i in range(1, count + 1):
                room_number = f"{prefix}{i}"
                
                # Double safety truncate
                if len(room_number) > 10:
                    room_number = room_number[:10]
                
                rooms_to_create.append(
                    Room(
                        room_number=room_number,
                        dormitory=instance,
                        room_type=rtype,
                        capacity=capacity
                    )
                )
        
        if rooms_to_create:
            created_rooms = Room.objects.bulk_create(rooms_to_create)
            
            # Now Create Beds for these rooms
            beds_to_create = []
            for room in created_rooms:
                for b_i in range(1, room.capacity + 1):
                    beds_to_create.append(
                        Bed(
                            bed_number=f"{room.room_number}-{b_i}",
                            room=room,
                            is_occupied=False
                        )
                    )
            
            if beds_to_create:
                Bed.objects.bulk_create(beds_to_create)

    def create(self, validated_data):
        configurations = validated_data.pop('room_configurations', [])
        
        # Remove total_rooms and total_beds from validated_data if present
        # since they will be calculated dynamically
        validated_data.pop('total_rooms', None)
        validated_data.pop('total_beds', None)
        
        # Set default values for the model fields (required by model)
        validated_data['total_rooms'] = 0
        validated_data['total_beds'] = 0
        
        dormitory = super().create(validated_data)
        
        # Create Rooms and Beds
        if configurations:
            self._process_room_configurations(dormitory, configurations)
            
        return dormitory

    def update(self, instance, validated_data):
        configurations = validated_data.pop('room_configurations', [])
        
        # Remove total_rooms and total_beds from validated_data if present
        # since they will be calculated dynamically
        validated_data.pop('total_rooms', None)
        validated_data.pop('total_beds', None)
        
        # Update instance fields (this handles manual changes to name, warden, etc.)
        instance = super().update(instance, validated_data)
        
        # Create Rooms and Beds from configurations
        if configurations:
            self._process_room_configurations(instance, configurations)
                
        return instance
